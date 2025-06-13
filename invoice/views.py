from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from .models import Invoice, PaymentTransaction
from .serializers import InvoiceSerializer, PaymentTransactionSerializer
from ticket.models import Ticket


class InvoiceCreateView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvoiceCreateWithTicketsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ticket_ids = request.data.get('ticket_ids', [])
        payment_method = request.data.get('payment_method', 'cod')

        if not ticket_ids:
            return Response({'error': 'No tickets selected'}, status=400)

        user = request.user
        with transaction.atomic():
            tickets = Ticket.objects.filter(id__in=ticket_ids, user=user, invoice__isnull=True)
            if not tickets.exists():
                return Response({'error': 'No available tickets'}, status=400)

            total_amount = sum([50000 for _ in tickets])  # Thay bằng ticket.price nếu có

            invoice = Invoice.objects.create(
                user=user,
                total_amount=total_amount,
                payment_method=payment_method,
            )

            tickets.update(invoice=invoice, status='confirmed')

        return Response(InvoiceSerializer(invoice).data)


class PaymentTransactionCreateView(generics.CreateAPIView):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentTransactionListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentTransaction.objects.filter(invoice__user=self.request.user)
