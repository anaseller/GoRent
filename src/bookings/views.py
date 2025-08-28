from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from .models import Booking, BookingStatusChoices
from .serializers import BookingSerializer
from src.listings.permissions import IsLandlord
from src.listings.models import Listing


class BookingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.all()

        if user.is_landlord:
            # The landlord sees bookings only for their own listings
            return queryset.filter(listing__landlord=user).select_related('listing', 'tenant')
        else:
            # The landlord sees only their own bookings
            return queryset.filter(tenant=user).select_related('listing', 'tenant')

    def perform_create(self, serializer):
        user = self.request.user
        check_in = serializer.validated_data.get('check_in_date')
        check_out = serializer.validated_data.get('check_out_date')

        # We get the listing id from the URL and check its existence
        listing_id = self.kwargs.get('listing_pk')
        try:
            listing = Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            raise serializers.ValidationError({"detail": "Listing not found."})

        # The landlord cannot book their own listing
        if user == listing.landlord:
            raise exceptions.PermissionDenied(
                "Landlords cannot book their own listings."
            )

        # Check for past dates
        if check_in < timezone.now().date():
            raise serializers.ValidationError(
                {"detail": "Check-in date cannot be in the past."}
            )

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            listing_id=listing_id,
            status__in=[BookingStatusChoices.PENDING, BookingStatusChoices.CONFIRMED]
        ).filter(
            Q(check_in_date__lt=check_out) & Q(check_out_date__gt=check_in)
        ).exists()

        if overlapping_bookings:
            raise serializers.ValidationError(
                {"detail": "This listing is not available for the requested dates."}
            )

        serializer.save(tenant=self.request.user, listing=listing)

class BookingConfirmRejectAPIView(generics.UpdateAPIView):
    """
    The landlord confirms or declines the booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        booking = self.get_object()

        # Check that the booking belongs to the current landlord
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
    The landlord cancels the booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        booking = self.get_object()

        # Check that the booking belongs to the current landlord
        if booking.tenant != self.request.user:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        # Check if the booking is already canceled or declined; it cannot be modified
        if booking.status in [BookingStatusChoices.CANCELLED, BookingStatusChoices.REJECTED]:
            return Response({"detail": "Cannot change status of this booking."},
                            status=status.HTTP_400_BAD_REQUEST)

        # If the booking is confirmed but less than 2 days remain until check-in, it cannot be canceled
        time_to_check_in = booking.check_in_date - timezone.now().date()
        if booking.status == BookingStatusChoices.CONFIRMED and time_to_check_in <= timedelta(days=2):
            return Response({"detail": "Cancellation is not allowed less than 2 days before check-in."},
                            status=status.HTTP_400_BAD_REQUEST)

        booking.status = BookingStatusChoices.CANCELLED
        booking.save()
        return Response(self.get_serializer(booking).data)


