# invoice/views.py
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Prefetch
from .models import Invoice, PaymentTransaction
from .serializers import InvoiceSerializer,InvoiceListSerializer
from ticket.models import Ticket
from ticket.serializers import TicketSerializer
from utils.customresponse import success_response, error_response
from vnpay_python.vnpay import vnpay
from utils.vn_mess import *

HOLD_TIMEOUT_MINUTES = 20

class HoldTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        ticket_ids = request.data.get('ticket_ids', [])
        if not ticket_ids:
            return error_response(NO_SELECT)
        user = request.user
        reserved_until = timezone.now() + timedelta(minutes=HOLD_TIMEOUT_MINUTES)   
        tickets = Ticket.objects.filter(id__in=ticket_ids, status='available', invoice__isnull=True)
        if tickets.count() != len(ticket_ids):
            return error_response(SEAT_NOT_AVAILABLE)
        tickets.update(status='pending', user=user, reserved_until=reserved_until)
        return success_response(SUCCESS_HOLD_SEAT, TicketSerializer(tickets, many=True).data)
class ReleaseTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        ticket_ids = request.data.get('ticket_ids', [])
        if not ticket_ids:
            return error_response(NO_SELECT)
        tickets = Ticket.objects.filter(id__in=ticket_ids, user=request.user, status='pending', invoice__isnull=True)
        if not tickets.exists():
            return error_response(NOT_FOUND.format(object="Vé"))
        tickets.update(status='available', user=None, reserved_until=None)
        return success_response(SUCCESS_RELEASE_SEAT)
class InvoiceCreateWithTicketsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        ticket_ids = request.data.get('ticket_ids', [])
        total_amount = request.data.get('total_amount')
        payment_method = request.data.get('payment_method', 'cod')
        passengers = request.data.get('passengers', [])  # Thêm
        if not ticket_ids or total_amount is None:
            return error_response(LACK_INFO)
        if len(passengers) != len(ticket_ids):
            return error_response(SEAT_DEFIRENT_PESS)
        with transaction.atomic():
            user = request.user
            tickets = Ticket.objects.filter(id__in=ticket_ids, user=user, invoice__isnull=True, status='pending')
            if tickets.count() != len(ticket_ids):
                return error_response(SEAT_NOT_TRUE)
            invoice = Invoice.objects.create(
                user=user,
                total_amount=total_amount,
                payment_method=payment_method,
                status='unpaid'
            )
            # Gán vé vào hóa đơn & cập nhật thông tin hành khách
            for ticket, passenger in zip(tickets, passengers):
                ticket.invoice = invoice
                ticket.passenger_name = passenger.get('name')
                ticket.passenger_phone = passenger.get('phone')
                ticket.passenger_email = passenger.get('email')
                ticket.pickup_point = passenger.get('pickup_point')  # 👈 THÊM DÒNG NÀY
                ticket.save()
            return success_response(CREATE_SUCCESS.format(object="hóa đơn"), InvoiceSerializer(invoice).data)
class VnpayPaymentUrlView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        invoice_id = request.data.get("invoice_id")
        if not invoice_id:
            return error_response(LACK_ID_INVOICE)
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
        except Invoice.DoesNotExist:
            return error_response(NOT_FOUND.format(object="hóa đơn"))
        vnp = vnpay()
        txn_ref = f"{invoice.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        vnp.requestData = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': settings.VNPAY_TMN_CODE,
            'vnp_Amount': int(invoice.total_amount) * 100,
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': txn_ref,
            'vnp_OrderInfo': f"Thanh toán hóa đơn #{invoice.id}",
            'vnp_OrderType': 'topup',
            'vnp_Locale': 'vn',
            'vnp_ReturnUrl': settings.VNPAY_RETURN_URL,
            'vnp_IpAddr': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            'vnp_CreateDate': timezone.now().strftime('%Y%m%d%H%M%S'),
        }
        payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
        return success_response(URL_SUCCESS, {"payment_url": payment_url})
@csrf_exempt
@api_view(["GET"])
def vnpay_return(request):
    vnp = vnpay()
    vnp.responseData = request.GET.dict()
    txn_ref = request.GET.get("vnp_TxnRef")
    invoice_id = txn_ref.split("_")[0] if txn_ref else None
    if not invoice_id:
        return HttpResponseBadRequest("Thiếu mã hóa đơn.")
    if not vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
        return HttpResponse("Sai checksum.", status=400)
    if vnp.responseData.get("vnp_ResponseCode") == "00":
        try:
            with transaction.atomic():
                invoice = Invoice.objects.select_for_update().get(id=invoice_id)
                if invoice.status != "paid":
                    invoice.status = "paid"
                    invoice.save()
                    Ticket.objects.filter(invoice=invoice).update(status="confirmed")
                    PaymentTransaction.objects.create(
                        invoice=invoice,
                        transaction_id=vnp.responseData.get("vnp_TransactionNo"),
                        amount=int(vnp.responseData.get("vnp_Amount", 0)) // 100
                    )
            return redirect(settings.VNPAY_FRONTEND_SUCCESS_URL)
        except Invoice.DoesNotExist:
            return HttpResponse("Hóa đơn không tồn tại.", status=404)
    return redirect(settings.VNPAY_FRONTEND_FAIL_URL)
class UserInvoiceListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        invoices = Invoice.objects.filter(user=request.user).order_by('-created_at')
        serializer = InvoiceListSerializer(invoices, many=True)
        return success_response(GET_SUCCESS.format(object="Hóa đơn"), serializer.data)
class InvoiceLookupView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return error_response(LACK_INFO_INVOICE)
        try:
            invoices = Invoice.objects.prefetch_related(
                Prefetch(
                    'ticket_set',
                    queryset=Ticket.objects.select_related('trip__route', 'trip__vehicle')
                )
            ).filter(Q(id=code) | Q(ticket__id=code)).distinct()
            if not invoices.exists():
                return success_response(NOT_FOUND)
            serializer = InvoiceListSerializer  (invoices, many=True)
            return success_response(GET_DETAIL_SUCCESS, serializer.data)
        except Exception as e:
            return error_response(str(e))