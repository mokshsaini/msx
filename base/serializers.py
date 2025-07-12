from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from .models import *


# class UserSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = User
#         fields = "__all__"
        
#     def create(self, validated_data):    # here we use create() becoz we want to hash password using create_user(), otherwise password don't get saved in hash format
#         return User.objects.create_user(**validated_data)
    
#     def validate(self, data):
#         new = User.objects.filter(Q(username=data.get('username')) | Q(email=data.get('email')))
#         if new.count():
#             raise serializers.ValidationError("username or email already exists!")
#         return data             # compulsory to return data in olv


# class ListingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Listing
#         fields = "__all__"

#     def validate_user(self, value):     #flv
#         new = Listing.objects.filter(user=value)
#         if new.count() > 5 :
#             raise serializers.ValidationError("Active Listings limit exceeded!")
#         return value        # compulsory to return data in flv

class ActiveListingsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='category', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='active_listings-detail')  
    total_bids = serializers.SerializerMethodField()
    is_current_bid = serializers.SerializerMethodField()
    class Meta:
        model = Listing
        # exclude = ['is_active', 'user']
        fields = ['id', 'category', 'url', 'total_bids', 'is_current_bid', 'title', 'description', 'minimum_bidvalue', 'created_at', 'updated_at', 'comment_set']

    def get_total_bids(self, instance):
        return instance.bid_set.count()
    
    def get_is_current_bid(self, instance):
        highest_bid = instance.bid_set.order_by('-bidvalue').first()
        if highest_bid:                                                 # i.e. highest_bid isn't None
            return True if self.context.get('request').user == highest_bid.user else False
        return False          
    
class MyListingsSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(slug_field='category', queryset = Category.objects.all())      # if not specified then it will treat category as category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), view_name='category-detail')
    url = serializers.HyperlinkedIdentityField(view_name='my_listings-detail')          # here we have to specify url attribute becoz by default drf takes view_name as <model-name>-detail but in actual it is <basename>-detail. so you have to specify view_name in url field if <model-name> != <basename>
    total_bids = serializers.SerializerMethodField()
    class Meta:
        model = Listing
        exclude = ['is_active', 'user']
        
    def get_total_bids(self, instance):
        return instance.bid_set.count()

    def validate_user(self, value):
        if value is None:
            return self.context.get('request').user
        
    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        