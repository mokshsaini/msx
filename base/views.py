from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


# class ActiveListingsView(APIView):
#     def get(self, request):
#         if request.user:
#             active_listings = Listing.objects.exclude(user=request.user, is_active=False)
#         else:
#             active_listings = Listing.objects.exclude(is_active=False)
#         serializer = ListingSerializer(data=active_listings)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class ActiveListingsViewSet(ReadOnlyModelViewSet):
    serializer_class = ActiveListingsSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if self.request.user:
            active_listings = Listing.objects.exclude(user=self.request.user.id).exclude(is_active=False)
        else:
            active_listings = Listing.objects.exclude(is_active=False)
        return active_listings

# class ClosedListingsView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         closed_listings = Listing.objects.filter(is_active=False)
#         serializer = ListingSerializer(data=closed_listings)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

class ClosedListingsViewSet(ReadOnlyModelViewSet):
    serializer_class = ActiveListingsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Listing.objects.exclude(is_active=True)
    

class MyListingsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = MyListingsSerializer

    def get_queryset(self):
        return Listing.objects.filter(user=self.request.user).order_by('is_active')


class CommentViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(listing=pk).order_by('is_active')

