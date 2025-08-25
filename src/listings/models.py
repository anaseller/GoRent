from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from src.users.models import BaseFields
from .choices import HousingTypeChoices, ListingStatusChoices

User = get_user_model()

class Listing(BaseFields):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255) # !доб валидацию и нормализацию
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    num_rooms = models.PositiveIntegerField(default=1)
    housing_type = models.CharField(max_length=50, choices=HousingTypeChoices.choices,
                                    default=HousingTypeChoices.APARTMENT)
    status = models.CharField(max_length=20, choices=ListingStatusChoices.choices, default=ListingStatusChoices.ACTIVE)

    def __str__(self):
        return self.title

