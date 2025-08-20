from rest_framework import generics, permissions
from .models import Listing
from .serializers import ListingSerializer
from .permissions import IsLandlord


class ListingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

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