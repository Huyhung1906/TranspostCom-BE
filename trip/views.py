from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import tripserializer
from .models import Trip
from utils.customresponse import *
from utils.vn_mess import *
from ticket.models import Ticket 
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime, time,timedelta
from django.utils.dateparse import parse_date, parse_datetime
from ticket.serializers import ticketserializer  # Import serializer vé


class createtripview(APIView):
    def post(self, request, format=None):
        serializer = tripserializer(data=request.data)
        if serializer.is_valid():
            trip = self.create_trip(serializer)
            tickets_data = self.create_tickets_for_trip(trip)
            
            response_data = {
                "trip": tripserializer(trip).data,
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
        tickets_data = ticketserializer(tickets, many=True).data
        return tickets_data
class updatetripview(APIView):
    def put(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)
        serializer = tripserializer(trip, data=request.data, partial=True)
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
            # Kiểm tra trùng lịch (ngoại trừ chính trip đang update)
            overlapping_trips = Trip.objects.filter(
                is_active=True,
                departure_time__lt=arrival_time,
                arrival_time__gt=departure_time
            ).exclude(pk=trip.pk).filter(
                Q(driver=driver) | Q(vehicle=vehicle)
            )
            if overlapping_trips.exists():
                return error_response(BUSY)

            # Kiểm tra điểm xuất phát hợp lệ
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

            # Cập nhật chuyến
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="Chuyến"), serializer.data)

        return error_response(serializer.errors, UPDATE_ERROR.format(object="Chuyến"))

class deletetripview(APIView):
    def delete(self, request, pk):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Chuyến"))
        serializer = tripserializer(trip,data = request.data,partial= True)
        trip.delete()
        if serializer.is_valid():
            return success_response(DELETE_SUCCESS.format(object="Chuyến"),serializer.data)
        return error_response(serializer.errors)
class tripbydateview(APIView):
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
        serializer = tripserializer(trips, many=True)
        return success_response(FOUND_TRIPS_BY_DATE.format(count=len(serializer.data), date=date_str),data=serializer.data)
class tripbytimeondayview(APIView):
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
        serializer = tripserializer(trips, many=True)
        return success_response(FOUND_TRIPS_BY_TIME_ON_DAY.format(count=len(serializer.data),start_time=start_time_str,date=date_str),data=serializer.data)   
    
class tripbyroutebiew(APIView):
    def get(self, request):
        route_id = request.query_params.get('route_id')
        if not route_id:
            return error_response(MISSING_PARAM.format(params="route_id"))
        
        try:
            trips = Trip.objects.filter(route__id=route_id)
            serializer = tripserializer(trips, many=True)
            return success_response(
                FOUND_TRIPS_BY_ROUTE.format(count=len(serializer.data), route_id=route_id),
                data=serializer.data
            )
        except Exception as e:
            return error_response(str(e))
class createmultipletripsview(APIView):
    def post(self, request):
        try:
            route_id = request.data['route_id']
            vehicle_id = request.data['vehicle_id']
            driver_id = request.data['driver_id']
            start_date = parse_date(request.data['start_date'])
            end_date = parse_date(request.data['end_date'])
            departure_time = datetime.strptime(request.data['time'], "%H:%M").time()
        except KeyError as e:
            return error_response(MISSING_PARAM.format(param=str(e)))
        except ValueError:
            return error_response(INVALID_DATE_TIME_FORMAT)

        if start_date > end_date:
            return error_response(START_DATE_GREATER_THAN_END_DATE)

        trips_created = []
        current_date = start_date
        while current_date <= end_date:
            departure_datetime = datetime.combine(current_date, departure_time)
            trip = Trip.objects.create(
                route_id=route_id,
                vehicle_id=vehicle_id,
                driver_id=driver_id,
                departure_time=departure_datetime
            )
            trips_created.append(trip)
            current_date += timedelta(days=1)

        serializer = tripserializer(trips_created, many=True)
        return success_response(
            CREATED_MULTIPLE_TRIPS.format(
                count=len(trips_created),
                start_date=start_date,
                end_date=end_date,
                time=departure_time.strftime("%H:%M")
            ),
            data=serializer.data
        )
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
        serializer = tripserializer(trip)
        return success_response(
            UPDATE_SUCCESS.format(object="Trạng thái Chuyến đi"),
            data=serializer.data
        )
class starttripview(APIView):
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
