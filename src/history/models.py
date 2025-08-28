from django.db import models
from django.contrib.auth import get_user_model
from src.listings.models import Listing

User = get_user_model()

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    search_query = models.CharField(max_length=255, null=True, blank=True)
    action_type = models.CharField(max_length=50) # 'view', 'search'
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "history"
        ordering = ['-timestamp']

    def __str__(self):
        if self.action_type == 'view':
            return f"Viewed {self.listing.title} by {self.user.email if self.user else 'Guest'} at {self.timestamp}"
        return f"Searched for '{self.search_query}' by {self.user.email if self.user else 'Guest'} at {self.timestamp}"