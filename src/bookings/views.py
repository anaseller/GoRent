from rest_framework import generics, permissions
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            return Booking.objects.filter(listing__landlord=user)
        else:
            return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)