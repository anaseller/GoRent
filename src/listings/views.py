from rest_framework import generics, permissions
from .models import Listing
from .serializers import ListingSerializer
from .permissions import IsLandlord
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter


class ListingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ListingFilter

    def get_permissions(self):
        # все могут просматривать
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        # создавать объявления может только арендодатель
        return [IsLandlord()]


class ListingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsLandlord]