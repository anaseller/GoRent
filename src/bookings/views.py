from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Booking, BookingStatusChoices
from .serializers import BookingSerializer
from src.listings.permissions import IsLandlord


class BookingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_landlord:
            # Арендодатель видит бронирования для своих объявлений
            return Booking.objects.filter(listing__landlord=user)
        # Арендатор видит только свои бронирования
        return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class BookingConfirmRejectAPIView(generics.UpdateAPIView):
    """
    Арендодатель подтверждает или отклоняет бронирование
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        booking = self.get_object()

        # проверка, что бронирование принадлежит текущему арендодателю
        if booking.listing.landlord != self.request.user:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in [BookingStatusChoices.CONFIRMED, BookingStatusChoices.REJECTED]:
            return Response({"detail": "Invalid status. Must be 'confirmed' or 'rejected'."},
                            status=status.HTTP_400_BAD_REQUEST)

        if booking.status != BookingStatusChoices.PENDING:
            return Response({"detail": "Cannot change status of a booking that is not 'pending'."},
                            status=status.HTTP_400_BAD_REQUEST)

        booking.status = new_status
        booking.save()
        return Response(self.get_serializer(booking).data)


class BookingCancelAPIView(generics.UpdateAPIView):
    """
    Арендатор отменеят бронирование
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        booking = self.get_object()

        # проверка, что бронирование принадлежит текущему арендатору
        if booking.tenant != self.request.user:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        if booking.status not in [BookingStatusChoices.PENDING, BookingStatusChoices.CONFIRMED]:
            return Response({"detail": "Cannot cancel a booking that is not 'pending' or 'confirmed'."},
                            status=status.HTTP_400_BAD_REQUEST)

        booking.status = BookingStatusChoices.CANCELLED
        booking.save()
        return Response(self.get_serializer(booking).data)


