from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny 
from .serializers import LoginSerializer
from utils.vn_mess import *
from utils.customresponse import success_response,error_response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(REGISTER_SUCCESS)
        return error_response(serializer.errors)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Tạo refresh và access token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            data = {
                "user": UserSerializer(user).data,
                "access_token": access_token
            }

            # Tạo response
            response = success_response(LOGIN_SUCCESS,data)

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,               
                samesite='Lax',
                max_age=7 * 24 * 60 * 60,  
                path='/' 
            )
            return response

        return error_response(serializer.errors)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        print("🔎 Refresh token nhận được:", refresh_token)

        if not refresh_token:
            return error_response(NOT_FOUND.format(object="refresh token"))

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            user = User.objects.get(id=token['user_id'])
            data = {
                "access_token": access_token
            }
            response = success_response(
                REFRESH_TOKEN_SUCCESS,
                data
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=7 * 24 * 60 * 60,
                path='/'
            )
            return response

        except Exception as e:
            return error_response(INVALID_TOKEN)

class ListUsersView(APIView):
    def get(self, request):
        user = User.objects.all()
        if not user.exists():
            return error_response(NOT_FOUND.format(object="Người dùng"))
        
        serializer = UserSerializer(user, many=True)
        return success_response(GET_SUCCESS.format(object="Người dùng"), serializer.data)

@api_view(['GET'])
def get_user_by_id_view(request, id):
    user = User.objects.filter(id=id)
    serializer = UserSerializer(user, many=True)
    if not user.exists():
        return error_response(NOT_FOUND.format(object=f"Người dùng id:{id}"))
    return success_response(GET_DETAIL_SUCCESS.format(object=f"Người dùng id:{id}"),serializer.data)

@api_view(['GET'])
def get_user_by_token_view(request, accesstoken):
    try:
        user = User.objects.get(accesstoken=accesstoken)
    except User.DoesNotExist:
        return error_response(NOT_FOUND.format(object="Người dùng"))

    serializer = UserSerializer(user)
    return success_response(GET_DETAIL_SUCCESS.format(object="Người dùng"), serializer.data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.headers)  # DEBUG

        user = request.user  # Django tự lấy user từ access_token trong header
        data = {
            "user": UserSerializer(user).data
        }
        return success_response(GET_DETAIL_SUCCESS.format(object="Người dùng"), data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            # Xóa cookie refresh_token ở trình duyệt
            response = success_response(LOGOUT_SUCCESS)
            response.delete_cookie('refresh_token')

            return response
        except Exception as e:
            return error_response(SERVER_ERROR)
        
class UpdateUserView(APIView):
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Người dùng"))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(UPDATE_SUCCESS.format(object="Người dùng"),serializer.data)
        return error_response(serializer.errors)
    
class DeleteUserView(APIView):
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return error_response(NOT_FOUND.format(object="Người dùng"))
        serializer = UserSerializer(user, data=request.data, partial=True)
        user.delete()
        if serializer.is_valid():
            serializer.save()
            return success_response(DELETE_SUCCESS.format(object="Người dùng"),serializer.data)
        return error_response(serializer.errors)
