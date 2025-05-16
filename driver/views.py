from django.shortcuts import render
from .serializers import DriverSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Driver
from utils.vn_mess import *
from utils.customresponse import *

class CreateDriverView(APIView):
    def post(seft, request):
        serializer = DriverSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(CREATE_SUCCESS,serializer.data)
        return error_response(serializer.errors)
        
class updatedriverview(APIView):
    def put(self, request,pk):
        try:
            driver = Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Tài xế"))
        serializer = DriverSerializer(instance=driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="thông tin Tài xế"),serializer.data)
        return error_response(serializer.error_messages)
    
class listdriverview(APIView):
    def get(self, request):
        driver = Driver.objects.all()
        if not driver.exists():
            return error_response(NOT_FOUND.format(object="Tài xế"))
        serializer = DriverSerializer(driver, many=True)
        return success_response(GET_SUCCESS.format(object="Tài xế"), serializer.data)
    
class deletedriverview(APIView):
    def delete(self, request, pk):
        try:
            driver = Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Tài xế"))
        serializer = DriverSerializer(driver,data = request.data,partial= True)
        driver.delete()
        if serializer.is_valid():
            return success_response(DELETE_SUCCESS.format(object="Tài xế"),serializer.data)
        return error_response(serializer.errors)
    
@api_view(['GET'])
def getdriverbyidview(request,id):
    driver = Driver.objects.filter(id=id)
    serializer = DriverSerializer(driver, many = True)
    if not driver.exists():
        return error_response(NOT_FOUND.format(object=f"Tài xế id: {id}"))
    return success_response(GET_DETAIL_SUCCESS.format(object=f"Tài xế id: {id}"),serializer.data)