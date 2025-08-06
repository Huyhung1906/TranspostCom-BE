from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TripSerializer
from .models import Trip
from utils.customresponse import *
from utils.vn_mess import *
from ticket.models import Ticket 
from django.db.models import Q,Count
from django.shortcuts import get_object_or_404
from datetime import datetime, time,timedelta
from django.utils.dateparse import parse_date, parse_datetime
from ticket.serializers import TicketSerializer  # Import serializer vé
from ticket.models import Ticket
from driver.models import Driver
from decimal import Decimal
from route.models import Route
from vehicle.models import Vehicle

class CreateTripView(APIView):
    def post(self, request, format=None):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            trip = self.create_trip(serializer)
            tickets_data = self.create_tickets_for_trip(trip)
            response_data = {
                "trip": TripSerializer(trip).data,
                "tickets": tickets_data
            }
            return success_response(CREATE_SUCCESS.format(object="Chuyến"), response_data)
        return error_response(serializer.errors, CREATE_ERROR)
    def create_trip(self, serializer):
        departure_time = serializer.validated_data.get('departure_time')
        route = serializer.validated_data.get('route')
        vehicle = serializer.validated_data.get('vehicle')
        driver = serializer.validated_data.get('driver')
        arrival_time = self.calculate_arrival_time(departure_time, route.estimated_time)
        self.check_schedule_conflicts(departure_time, arrival_time, driver, vehicle)
        self.check_route_validity(departure_time, route, driver, vehicle)
        trip = serializer.save(arrival_time=arrival_time)
        return trip
    def calculate_arrival_time(self, departure_time, estimated_time):
        return departure_time + timedelta(
            hours=estimated_time.hour,
            minutes=estimated_time.minute,
            seconds=estimated_time.second
        )
    def check_schedule_conflicts(self, departure_time, arrival_time, driver, vehicle):
        overlapping_trips = Trip.objects.filter(
            is_active=True,
            departure_time__lt=arrival_time,
            arrival_time__gt=departure_time
        ).filter(
            Q(driver=driver) | Q(vehicle=vehicle)
        )
        if overlapping_trips.exists():
            raise Exception(BUSY)  # hoặc return error_response ngay trong hàm gọi (cần xử lý phù hợp)

    def check_route_validity(self, departure_time, route, driver, vehicle):
        last_trip = Trip.objects.filter(
            is_active=True,
            departure_time__lt=departure_time,
            driver=driver,
            vehicle=vehicle
        ).order_by('-departure_time').first()

        if last_trip and route.departure_point != last_trip.route.destination_point:
            raise Exception(INVALID_ROUTE_LOCATION.format(
                current_location=last_trip.route.destination_point,
                departure_location=route.departure_point
            ))
    def create_tickets_for_trip(self, trip):
        vehicle = trip.vehicle
        if vehicle and vehicle.chair:
            tickets = []
            for seat_num in range(1, vehicle.chair + 1):
                ticket = Ticket(
                    trip=trip,
                    seat_number=str(seat_num),
                    status='available',
                    passenger_name='',
                    passenger_phone='',
                    passenger_email='',
                )
                tickets.append(ticket)
            Ticket.objects.bulk_create(tickets)
        
        tickets = Ticket.objects.filter(trip=trip)
        tickets_data = TicketSerializer(tickets, many=True).data
        return tickets_data
class UpdateTripView(APIView):
    def put(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)
        serializer = TripSerializer(trip, data=request.data, partial=True)
        if serializer.is_valid():
            departure_time = serializer.validated_data.get('departure_time', trip.departure_time)
            route = serializer.validated_data.get('route', trip.route)
            vehicle = serializer.validated_data.get('vehicle', trip.vehicle)
            driver = serializer.validated_data.get('driver', trip.driver)
            est_time = route.estimated_time
            arrival_time = departure_time + timedelta(
                hours=est_time.hour,
                minutes=est_time.minute,
                seconds=est_time.second
            )
            overlapping_trips = Trip.objects.filter(
                is_active=True,
                departure_time__lt=arrival_time,
                arrival_time__gt=departure_time
            ).exclude(pk=trip.pk).filter(   
                Q(driver=driver) | Q(vehicle=vehicle)
            )
            if overlapping_trips.exists():
                return error_response(BUSY)
            last_trip = Trip.objects.filter(
                is_active=True,
                departure_time__lt=departure_time,
                driver=driver,
                vehicle=vehicle
            ).exclude(pk=trip.pk).order_by('-departure_time').first()
            if last_trip and route.departure_point != last_trip.route.destination_point:
                return error_response(INVALID_ROUTE_LOCATION.format(
                    current_location=last_trip.route.destination_point,
                    departure_location=route.departure_point
                ))
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="Chuyến"), serializer.data)
        return error_response(serializer.errors, UPDATE_ERROR.format(object="Chuyến"))
class DeleteTripView(APIView):
    def delete(self, request, pk):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Chuyến"))
        serializer = TripSerializer(trip,data = request.data,partial= True)
        trip.delete()
        if serializer.is_valid():
            return success_response(DELETE_SUCCESS.format(object="Chuyến"),serializer.data)
        return error_response(serializer.errors)
class TripbyDateView(APIView):
    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return error_response(MISSING_PARAM.format(params="Date"))
        try:
            date_obj = parse_date(date_str)
            if not date_obj:
                raise ValueError()
        except ValueError:
            return error_response(INVALID_DATE)
        trips = Trip.objects.filter(departure_time__date=date_obj)
        serializer = TripSerializer(trips, many=True)
        return success_response(FOUND_TRIPS_BY_DATE.format(count=len(serializer.data), date=date_str),data=serializer.data)
class TripbyTimeonDayView(APIView):
    def get(self, request):
        date_str = request.query_params.get('date')
        start_time_str = request.query_params.get('start_time')
        if not all([date_str, start_time_str]):
            return error_response(MISSING_PARAM.format(params="date/start_time"))

        try:
            date_obj = parse_date(date_str)
            start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
        except ValueError:
            return error_response(INVALID_DATE_TIME_FORMAT)

        trips = Trip.objects.filter(
            departure_time__date=date_obj,
            departure_time__time__gte=start_time_obj,
        )
        serializer = TripSerializer(trips, many=True)
        return success_response(FOUND_TRIPS_BY_TIME_ON_DAY.format(count=len(serializer.data),start_time=start_time_str,date=date_str),data=serializer.data)   
    
class TripbyRouteView(APIView):
    def get(self, request):
        route_id = request.query_params.get('route_id')
        if not route_id:
            return error_response(MISSING_PARAM.format(params="route_id"))
        
        try:
            trips = Trip.objects.filter(route__id=route_id)
            serializer = TripSerializer(trips, many=True)
            return success_response(
                FOUND_TRIPS_BY_ROUTE.format(count=len(serializer.data), route_id=route_id),
                data=serializer.data
            )
        except Exception as e:
            return error_response(str(e))
class TripbyRouteDateView(APIView):
    def get(self, request):
        route_id = request.query_params.get('route_id')
        date_str = request.query_params.get('date')  # Expecting 'YYYY-MM-DD'

        if not route_id or not date_str:
            return error_response(MISSING_PARAM.format(params="route_id và date"))

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            start_datetime = datetime.combine(date_obj, datetime.min.time())
            end_datetime = datetime.combine(date_obj, datetime.max.time())

            trips = Trip.objects.filter(
                route__id=route_id,
                departure_time__range=(start_datetime, end_datetime),
                is_active=True
            ).annotate(
                total_tickets=Count('ticket'),
                sold_tickets=Count('ticket', filter=~Q(ticket__status='available'))
            ).order_by('departure_time')

            serializer = TripSerializer(trips, many=True)
            return success_response(
                FOUND_TRIPS_BY_ROUTE.format(count=len(serializer.data), route_id=route_id),
                data=serializer.data
            )
        except ValueError:
            return error_response("Sai định dạng ngày. Định dạng đúng là YYYY-MM-DD.")
        except Exception as e:
            return error_response(str(e))

class CreateMutiTripView(APIView):
    def post(self, request):
        try:
            route_id = request.data['route_id']
            vehicle_id = request.data['vehicle_id']
            driver_id = request.data['driver_id']
            start_date = parse_date(request.data['start_date'])
            end_date = parse_date(request.data['end_date'])
            departure_time = datetime.strptime(request.data['time'], "%H:%M").time()
            price = Decimal(request.data['price'])  # 🔥 Thêm dòng này

        except KeyError as e:
            return error_response(MISSING_PARAM.format(param=str(e)))
        except ValueError:
            return error_response(INVALID_DATE_TIME_FORMAT)

        if start_date > end_date:
            return error_response(START_DATE_GREATER_THAN_END_DATE)

        try:
            route = Route.objects.get(id=route_id)
            vehicle = Vehicle.objects.get(id=vehicle_id)
            driver = Driver.objects.get(id=driver_id)
        except Route.DoesNotExist:
            return error_response("Tuyến không tồn tại")
        except Vehicle.DoesNotExist:
            return error_response("Xe không tồn tại")
        except Driver.DoesNotExist:
            return error_response("Tài xế không tồn tại")
        trips_created = []
        current_date = start_date
        while current_date <= end_date:
            departure_datetime = datetime.combine(current_date, departure_time)
            arrival_time = self.calculate_arrival_time(departure_datetime, route.estimated_time)

            trip = Trip.objects.create(
                route=route,
                vehicle=vehicle,
                driver=driver,
                departure_time=departure_datetime,
                arrival_time=arrival_time,
                price=price
            )
            self.create_tickets_for_trip(trip)
            trips_created.append(trip)
            current_date += timedelta(days=1)
        serializer = TripSerializer(trips_created, many=True)
        return success_response(
            CREATED_MULTIPLE_TRIPS.format(
                count=len(trips_created),
                start_date=start_date,
                end_date=end_date,
                time=departure_time.strftime("%H:%M")
            ),
            sdata=serializer.data
        )
    def calculate_arrival_time(self, departure_time, estimated_time):
        return departure_time + timedelta(
            hours=estimated_time.hour,
            minutes=estimated_time.minute,
            seconds=estimated_time.second
        )
    def create_tickets_for_trip(self, trip):
        vehicle = trip.vehicle
        if vehicle and vehicle.chair:
            tickets = [
                Ticket(
                    trip=trip,
                    seat_number=str(seat_num),
                    status='available',
                    passenger_name='',
                    passenger_phone='',
                    passenger_email='',
                )
                for seat_num in range(1, vehicle.chair + 1)
            ]
            Ticket.objects.bulk_create(tickets)
class UpdateTripIsActiveView(APIView):
    def patch(self, request, pk):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Chuyến đi"))

        is_active = request.data.get('is_active')
        if is_active is None:
            return error_response(MISSING_PARAM.format(param="is_active"))

        if not isinstance(is_active, bool):
            return error_response(INVALID_ACTIVE)
        trip.is_active = is_active
        trip.save()
        serializer = TripSerializer(trip)
        return success_response(
            UPDATE_SUCCESS.format(object="Trạng thái Chuyến đi"),
            data=serializer.data
        )
class StartTripView(APIView):
    def post(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)

        # Cập nhật notes khi xuất phát
        trip.notes = START
        trip.save()
        data = {
            "trip_id": trip.id,
            "notes": trip.notes
        }
        return success_response(UPDATE_SUCCESS.format(object="Trạng thái xuất phát"),data)

class TripDetailAPIView(APIView):
    def get(self, request, trip_id):
        try:
            trip = Trip.objects.select_related('route', 'vehicle', 'driver').get(id=trip_id)
        except Trip.DoesNotExist:
            return error_response(NOT_FOUND)

        tickets = Ticket.objects.filter(trip=trip)
    
        trip_data = TripSerializer(trip).data
        trip_data['tickets'] = TicketSerializer(tickets, many=True).data
        return success_response(GET_SUCCESS, {
            'trip': trip_data
        })
