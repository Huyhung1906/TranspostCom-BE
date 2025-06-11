from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from .serializers import TicketSerializer
from utils.customresponse import *
from utils.vn_mess import *
from trip.models import Trip
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import UpdateAPIView
class CreateTicketView(APIView):
    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(CREATE_SUCCESS.format(object="Vé"),serializer.data)
        return error_response(serializer.errors,CREATE_ERROR)
    
class GetListTicketbyTrip(APIView):
    def get(self, request, trip_id):
        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Chuyến đi"))
        tickets = Ticket.objects.filter(trip=trip)
        serializer = TicketSerializer(tickets, many=True)
        return success_response(GET_SUCCESS.format(object="Vé"),serializer.data)
    
class UpdateTicketView(APIView):
    def put(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Vé"))
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="Vé"),serializer.data)
        return error_response(serializer.errors)
    
class DeleteTicketView(APIView):
    def delete(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Vé"))
        if ticket.invoice is not None:
            return error_response(NOT_DELETE_TICKET_INVOICE)
        # Xoá thông tin hành khách, giữ số ghế
        ticket.status = "available"  # hoặc "trống"
        ticket.passenger_name = ""
        ticket.passenger_phone = ""
        ticket.passenger_email = ""
        ticket.invoice = None
        ticket.user = None
        ticket.save()
        return success_response(DELETE_SUCCESS.format(object="Vé đã mua"))

class TicketDetailView(APIView):
    def get(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Vé"))
        serializer = TicketSerializer(ticket)
        return success_response(GET_DETAIL_SUCCESS.format(object="Vé"),serializer.data)
    
class MyTicketsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tickets = Ticket.objects.filter(user=user).select_related('trip')
        serializer = TicketSerializer(tickets, many=True)
        return Response({'data': serializer.data})