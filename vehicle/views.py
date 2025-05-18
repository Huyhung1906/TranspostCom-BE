from django.shortcuts import render
from .serializers import vehicleserializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Vehicle
from utils.vn_mess import *
from utils.customresponse import *

class createvehicleview(APIView):
    def post(seft, request):
        serializer = vehicleserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(CREATE_SUCCESS.format(object="Phương tiện"),serializer.data)
        return error_response(serializer.errors)
class updatevehicleview(APIView):
    def put(self, request,pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = vehicleserializer(instance=vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="thông tin Phương Tiện"),serializer.data)
        return error_response(serializer.error_messages)
    
class listvehicleview(APIView):
    def get(self, request):
        vehicle = Vehicle.objects.all()
        if not vehicle.exists():
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = vehicleserializer(vehicle, many=True)
        return success_response(GET_SUCCESS.format(object="Phương Tiện"), serializer.data)
    
class deletevehicleview(APIView):
    def delete(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = vehicleserializer(vehicle,data = request.data,partial= True)
        vehicle.delete()
        if serializer.is_valid():
            return success_response(DELETE_SUCCESS.format(object="Phương Tiện"),serializer.data)
        return error_response(serializer.errors)
    
@api_view(['GET'])
def getvehiclebyidview(request,id):
    vehicle = Vehicle.objects.filter(id=id)
    serializer = vehicleserializer(vehicle, many = True)
    if not vehicle.exists():
        return error_response(NOT_FOUND.format(object=f"Phương tiện id: {id}"))
    return success_response(GET_DETAIL_SUCCESS.format(object=f"Phương tiện id: {id}"),serializer.data)