from django.db import models
from django.conf import settings
from src.users.models import BaseFields


class Listing(BaseFields):
    HOUSING_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('room', 'Room'),
        ('villa', 'Villa'),
    ]

    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    num_rooms = models.PositiveSmallIntegerField(default=1)
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPES, default='apartment')

    def __str__(self):
        return self.title