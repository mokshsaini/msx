from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register('active-listings', ActiveListingsViewSet, basename='active_listings')
router.register('closed-listings', ClosedListingsViewSet, basename='closed_listings')
router.register('my-listings', MyListingsViewSet, basename='my_listings')
router.register('comments', CommentViewset, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)  # to allow format_suffix in url patterns # doesn't require with viewsets(routers) as it already includes it