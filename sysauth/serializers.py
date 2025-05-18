from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            }
    
    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Password and Confirm Password doesn't match!")
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Password and confirm password doesn't match!")
        return data


class UserResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("You are not a register user")
        uid = urlsafe_base64_encode(force_bytes(user.id))
        print('uid:', uid)
        token = PasswordResetTokenGenerator().make_token(user)
        print('token:', token)
        link = f"http://localhost:8000/api/user/reset-password/{uid}/{token}"
        # Send link through Email
        body = f"Click on the Link to reset your password: {link}"
        subject = "password reset link"
        to = user.email
        Util.send_email(data={"subject": subject, "to": to, "body": body})
        return value

