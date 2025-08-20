from django.db import models
from django.contrib.auth import get_user_model
from src.users.models import BaseFields
from src.listings.models import Listing

User = get_user_model()


class Review(BaseFields):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    class Meta:
        unique_together = ('listing', 'reviewer')

    def __str__(self):
        return f'Review for {self.listing.title} by {self.reviewer.name}'