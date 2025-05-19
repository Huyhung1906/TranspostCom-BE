from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import tripserializer
from .models import Trip
from utils.customresponse import *
from utils.vn_mess import *
from django.shortcuts import get_object_or_404
from datetime import datetime, time
from django.utils.dateparse import parse_date, parse_datetime

class createtripview(APIView):
    def post(self, request, format=None):
        serializer = tripserializer(data=request.data)
        if serializer.is_valid():
            trip = serializer.save()
            return success_response(CREATE_SUCCESS.format(object="Chuyến"),tripserializer(trip).data)
        return error_response(serializer.errors,CREATE_ERROR)
class updatetripview(APIView):
    def put(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)
        serializer = tripserializer(trip, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="Chuyến"),serializer.data)
        return error_response(serializer.errors,UPDATE_ERROR.format(object="Chuyến"))
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
