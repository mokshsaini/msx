from .views import *
from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('change-password', UserChangePasswordView.as_view(), name='chpswd'),
    path('reset-password-email', UserResetPasswordEmailView.as_view(), name='rspswdemail'),
    path('reset-password/<str:uid>/<str:token>', UserResetPasswordView.as_view(), name='rspswd'),

]
