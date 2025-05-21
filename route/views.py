from django.shortcuts import render
from .serializers import RouteSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Route
from utils.vn_mess import *
from utils.customresponse import *

class CreateRouteView(APIView):
    def post(seft, request):
        serializer = RouteSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(CREATE_SUCCESS.format(object="Tuyến đường"),serializer.data)
        return error_response(serializer.errors)
        
class UpdateRouteView(APIView):
    def put(self, request,pk):
        print("Request data:", request.data)
        try:
            route = Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Phương Tiện"))
        serializer = RouteSerializer(instance=route, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="thông tin Phương Tiện"),serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ListRouteView(APIView):
    def get(self, request):
        route = Route.objects.all()
        if not route.exists():
            return error_response(NOT_FOUND.format(object="Tuyến đường"))
        serializer = RouteSerializer(route, many=True)
        return success_response(GET_SUCCESS.format(object="Tuyến đường"), serializer.data)
    
class DeleteRouteView(APIView):
    def delete(self, request, pk):
        try:
            route = Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Tuyến đường"))
        serializer = RouteSerializer(route,data = request.data,partial= True)
        route.delete()
        if serializer.is_valid():
            return success_response(DELETE_SUCCESS.format(object="Tuyến đường"),serializer.data)
        return error_response(serializer.errors)
    
@api_view(['GET'])
def get_route_by_id_view(request,id):
    route = Route.objects.filter(id=id)
    serializer = RouteSerializer(route, many = True)
    if not route.exists():
        return error_response(NOT_FOUND.format(object=f"Tuyến đường id: {id}"))
    return success_response(GET_DETAIL_SUCCESS.format(object=f"Tuyến đường id: {id}"),serializer.data)