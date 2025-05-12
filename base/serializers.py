from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = "__all__"
        
    def create(self, validated_data):    # here we use create() becoz we want to hash password using create_user(), otherwise password don't get saved in hash format
        return User.objects.create_user(**validated_data)
    
    def validate(self, data):
        new = User.objects.filter(Q(username=data.get('username')) | Q(email=data.get('email')))
        if new.count():
            raise serializers.ValidationError("username or email already exists!")
        return data             # compulsory to return data in olv


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"

    def validate_user(self, value):     #flv
        new = Listing.objects.filter(user=value)
        if new.count() > 5 :
            raise serializers.ValidationError("Active Listings limit exceeded!")
        return value        # compulsory to return data in flv
