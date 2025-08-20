from django.db import models
from django.contrib.auth import get_user_model
from src.users.models import BaseFields
from src.listings.models import Listing

User = get_user_model()

class Booking(BaseFields):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_tenant')
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f'Booking for {self.listing.title} by {self.tenant.name}'