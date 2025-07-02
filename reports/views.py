from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view
from utils.customresponse import success_response, error_response
from ticket.models import Ticket
from trip.models import Trip
from invoice.models import Invoice
from collections import defaultdict


# 1. Thống kê tổng số vé (kể cả offline) và doanh thu theo tháng
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view
from utils.customresponse import success_response, error_response
from ticket.models import Ticket

@api_view(['GET'])
def ticket_sales_and_revenue_by_month(request):
    try:
        # Tổng số vé trong tháng (bất kể trạng thái)
        all_tickets = (
            Ticket.objects
            .annotate(month=TruncMonth('trip__departure_time'))
            .values('month')
            .annotate(total_tickets_in_month=Count('id'))
        )
        # Map để truy cập nhanh
        total_map = {
            item['month']: item['total_tickets_in_month']
            for item in all_tickets
        }

        # Vé đã bán + doanh thu
        confirmed_data = (
            Ticket.objects
            .filter(status='confirmed')
            .annotate(month=TruncMonth('trip__departure_time'))
            .values('month')
            .annotate(
                total_sold=Count('id'),
                total_revenue=Sum('trip__price')
            )
            .order_by('month')
        )

        # Tính phần trăm và ghép dữ liệu
        result = []
        for item in confirmed_data:
            month = item['month']
            total_in_month = total_map.get(month, 0)
            percentage = (item['total_sold'] / total_in_month) * 100 if total_in_month > 0 else 0

            result.append({
                "month": month,
                "total_sold": item['total_sold'],
                "total_revenue": item['total_revenue'],
                "total_tickets_in_month": total_in_month,
                "percentage": round(percentage, 2)
            })

        return success_response("Thống kê vé theo tháng thành công", result)

    except Exception as e:
        return error_response("Lỗi thống kê vé theo tháng", {"detail": str(e)})

# 2. Thống kê số vé được bán online theo tháng (dựa vào invoice)
@api_view(['GET'])
def online_ticket_sales_by_month(request):
    try:
        data = (
            Ticket.objects
            .filter(invoice__isnull=False, invoice__status='paid')
            .annotate(month=TruncMonth('invoice__created_at'))
            .values('month')
            .annotate(
                total_online_tickets=Count('id'),
                total_online_revenue=Sum('trip__price')
            )
            .order_by('month')
        )
        return success_response("Thống kê vé bán online theo tháng", list(data))
    except Exception as e:
        return error_response("Lỗi khi thống kê vé online", {"detail": str(e)})


# 3. Top 10 xe chạy nhiều chuyến nhất
@api_view(['GET'])
def top_vehicles(request):
    try:
        data = (
            Trip.objects
            .values(vehicle_name=F('vehicle__name'), license_plate=F('vehicle__licenseplate'))
            .annotate(total_trips=Count('id'))
            .order_by('-total_trips')[:10]
        )
        return success_response("Top xe chạy nhiều chuyến nhất", list(data))
    except Exception as e:
        return error_response("Lỗi khi thống kê xe", {"detail": str(e)})


# 4. Top 10 tài xế chạy nhiều chuyến nhất
@api_view(['GET'])
def top_drivers(request):
    try:
        data = (
            Trip.objects
            .values(driver_name=F('driver__fullname'), driver_phone=F('driver__phone'))
            .annotate(total_trips=Count('id'))
            .order_by('-total_trips')[:10]
        )
        return success_response("Top tài xế chạy nhiều chuyến nhất", list(data))
    except Exception as e:
        return error_response("Lỗi khi thống kê tài xế", {"detail": str(e)})

@api_view(['GET'])
def top_vehicles_by_month(request):
    try:
        data = (
            Trip.objects
            .annotate(month=TruncMonth('departure_time'))
            .values('month', 'vehicle__name', 'vehicle__licenseplate')
            .annotate(total_trips=Count('id'))
            .order_by('month', '-total_trips')
        )

        grouped = defaultdict(list)
        for item in data:
            month = item['month']
            grouped[month].append({
                'vehicle_name': item['vehicle__name'],
                'license_plate': item['vehicle__licenseplate'],
                'total_trips': item['total_trips']
            })

        result = []
        for month, vehicles in grouped.items():
            result.append({
                'month': month,
                'top_vehicles': vehicles[:10]
            })

        return success_response("Top 10 xe chạy nhiều nhất theo tháng", result)

    except Exception as e:
        return error_response("Lỗi khi thống kê xe theo tháng", {"detail": str(e)})


@api_view(['GET'])
def top_drivers_by_month(request):
    try:
        data = (
            Trip.objects
            .annotate(month=TruncMonth('departure_time'))
            .values('month', 'driver__fullname', 'driver__phone')
            .annotate(total_trips=Count('id'))
            .order_by('month', '-total_trips')
        )

        grouped = defaultdict(list)
        for item in data:
            month = item['month']
            grouped[month].append({
                'driver_name': item['driver__fullname'],
                'driver_phone': item['driver__phone'],
                'total_trips': item['total_trips']
            })

        result = []
        for month, drivers in grouped.items():
            result.append({
                'month': month,
                'top_drivers': drivers[:10]
            })

        return success_response("Top 10 tài xế chạy nhiều nhất theo tháng", result)

    except Exception as e:
        return error_response("Lỗi khi thống kê tài xế theo tháng", {"detail": str(e)})