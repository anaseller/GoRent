from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from src.bookings.models import Booking
from django.db import models
from django.utils import timezone


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_landlord:
                # арендодатель видит все отзывы на его объявления
                return Review.objects.filter(listing__landlord=user)
            else:
                # арендатор видит все отзывы на любые объявления
                return Review.objects.all()
        # для неаутентифицированных пользователей (они тоже могут смотреть)
        return Review.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        listing_id = self.request.data.get('listing')

        # проверка: может ли пользователь оставить отзыв
        # отзыв можно оставить только если была подтвержденная бронь и она уже завершилась
        has_booked = Booking.objects.filter(
            tenant=user,
            listing_id=listing_id,
            check_out_date__lt=timezone.now().date()
        ).exists()

        if not has_booked:
            raise permissions.PermissionDenied(
                "You can only leave a review for a listing you have booked and stayed at.")

        # автоматически устанавливаем пользователя как автора отзыва
        serializer.save(reviewer=user)