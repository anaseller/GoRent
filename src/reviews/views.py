from rest_framework import generics, permissions, exceptions
from .models import Review
from .serializers import ReviewSerializer
from src.bookings.models import Booking, BookingStatusChoices
from django.db import models
from django.utils import timezone


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_landlord:
                # The landlord sees all reviews for their listings
                return Review.objects.filter(listing__landlord=user)
            else:
                # The tenant sees all reviews for any listings
                return Review.objects.all()
        # For unauthenticated users (they can also view)
        return Review.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        listing = serializer.validated_data.get('listing')

        # Check that the user is not the landlord of their own listing
        if user == listing.landlord:
            raise exceptions.PermissionDenied(
                "Landlords cannot leave reviews on their own listings."
            )

        # Check that the user booked this listing and the booking is completed
        has_completed_booking = Booking.objects.filter(
            tenant=user,
            listing=listing,
            check_out_date__lt=timezone.now().date(),
            status=BookingStatusChoices.CONFIRMED
        ).exists()

        if not has_completed_booking:
            raise exceptions.PermissionDenied(
                "You can only review a listing after a completed booking."
            )

        # Check that the user has not yet left a review for this listing
        existing_review = Review.objects.filter(reviewer=user, listing=listing).exists()
        if existing_review:
            raise exceptions.PermissionDenied(
                "You have already submitted a review for this listing."
            )

        serializer.save(reviewer=user)