from django.shortcuts import render
from .serializers import VehicleSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Vehicle
from utils.vn_mess import *
from utils.customresponse import *

class CreateVehicleView(APIView):
    def post(seft, request):
        serializer = VehicleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(CREATE_SUCCESS.format(object="Phương tiện"),serializer.data)
        return error_response(serializer.errors)
class UpdateVehicleView(APIView):
    def put(self, request,pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = VehicleSerializer(instance=vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="thông tin Phương Tiện"),serializer.data)
        return error_response(serializer.error_messages)
    
class ListVehicleView(APIView):
    def get(self, request):
        vehicle = Vehicle.objects.all()
        if not vehicle.exists():
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = VehicleSerializer(vehicle, many=True)
        return success_response(GET_SUCCESS.format(object="Phương Tiện"), serializer.data)
    
class DeleteVehicleView(APIView):
    def delete(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = VehicleSerializer(vehicle,data = request.data,partial= True)
        vehicle.delete()
        if serializer.is_valid():
            return success_response(DELETE_SUCCESS.format(object="Phương Tiện"),serializer.data)
        return error_response(serializer.errors)
    
@api_view(['GET'])
def get_vehicle_by_id_view(request,id):
    vehicle = Vehicle.objects.filter(id=id)
    serializer = VehicleSerializer(vehicle, many = True)
    if not vehicle.exists():
        return error_response(NOT_FOUND.format(object=f"Phương tiện id: {id}"))
    return success_response(GET_DETAIL_SUCCESS.format(object=f"Phương tiện id: {id}"),serializer.data)