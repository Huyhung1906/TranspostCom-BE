from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','fullname','phone','role','email','is_active']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    def create(self, validated_data):
        role = validated_data.pop('role',2)
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
#Class xử lý đăng nhập trang người dùng (Login)    
class LoginSerializer   (serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:  
            raise serializers.ValidationError("Tài khoản không tồn tại.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Mật khẩu không đúng.")

        if not user.is_active:
            raise serializers.ValidationError("Tài khoản đã bị vô hiệu hóa.")

        data['user'] = user
        return data
