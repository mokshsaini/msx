from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from rest_framework.exceptions import ValidationError


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()        # user contains email
        token = get_tokens_for_user(user)
        return Response({"message": "Registration Successful!", 'token': token}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid()
        user = authenticate(request, **serializer.validated_data)       # user contains email
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"message": "login successful!", 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": {"non_field_errors": ["Email or Password is not Valid"]}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)


class UserResetPasswordEmailView(APIView):
    def post(self, request):
        serializer = UserResetPasswordEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password Reset Email Send Successfully!"}, status=status.HTTP_200_OK)


class UserResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=uid)
        except (User.DoesNotExist, DjangoUnicodeDecodeError):
            raise ValidationError("Token is invalid or expired!")
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError("Token is invalid or expired!")
        user.set_password(serializer.validated_data.get("password"))
        user.save()
        return Response({"message": "Password changed successfully!"})
    