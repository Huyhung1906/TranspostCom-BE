from django.shortcuts import render
from .serializers import busserializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Bus
from utils.vn_mess import *
from utils.customresponse import *

class createbusview(APIView):
    def post(seft, request):
        serializer = busserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(CREATE_SUCCESS.format(object="Phương tiện"),serializer.data)
        return error_response(serializer.errors)
class updatebusview(APIView):
    def put(self, request,pk):
        try:
            bus = Bus.objects.get(pk=pk)
        except Bus.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = busserializer(instance=bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="thông tin Phương Tiện"),serializer.data)
        return error_response(serializer.error_messages)
    
class listbusview(APIView):
    def get(self, request):
        bus = Bus.objects.all()
        if not bus.exists():
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = busserializer(bus, many=True)
        return success_response(GET_SUCCESS.format(object="Phương Tiện"), serializer.data)
    
class deletebusview(APIView):
    def delete(self, request, pk):
        try:
            bus = Bus.objects.get(pk=pk)
        except Bus.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = busserializer(bus,data = request.data,partial= True)
        bus.delete()
        if serializer.is_valid():
            return success_response(DELETE_SUCCESS.format(object="Phương Tiện"),serializer.data)
        return error_response(serializer.errors)
    
@api_view(['GET'])
def getbusbyidview(request,id):
    bus = Bus.objects.filter(id=id)
    serializer = busserializer(bus, many = True)
    if not bus.exists():
        return error_response(NOT_FOUND.format(object=f"Phương tiện id: {id}"))
    return success_response(GET_DETAIL_SUCCESS.format(object=f"Phương tiện id: {id}"),serializer.data)