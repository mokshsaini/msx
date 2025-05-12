from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
# router.register('activelistings', ActiveListingsViewset, basename='active_listings')

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    # # path('update_user', signup, name='signup'),
    # path('home', home, name='home'),
    # path('home/listing/<int:pk>', Listing_detail.as_view(), name='listing_detail'),s
    # path('', include(router.urls)),
    # path('', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)  # to allow format_suffix in url patterns