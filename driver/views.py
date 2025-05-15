from django.shortcuts import render
# Sự kiện thêm mới Artist ( Nghệ sĩ )
from .serializers import DriverSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Driver

class CreateDriverView(APIView):
    def post(self, request):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Thêm tài xế thành công!",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
class UpdateDriverView(APIView):
    def put(self, request,pk):
        serializer = DriverSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Cập nhập thông tin tài xế thành công.!",
                "data": {
                    "driver":serializer.data,
                },
                "status": status.HTTP_201_CREATED
            }, status = status.HTTP_201_CREATED)
        return Response({
            "message": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
class DeleteDriver(APIView):
    def delete(self, request, id):
        try:
            driver = Driver.objects.get(pk=id)
            fullname = driver.fullname
            driver.delete()
            return Response({
                "message": f"Xóa tài xế {fullname} thành công!",
                "status": status.HTTP_200_OK
                },
                status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response({
                            "message": f"Bài hát với id={artist_id} không tồn tại."},
                            status=status.HTTP_404_NOT_FOUND)