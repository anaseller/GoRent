from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_email = serializers.ReadOnlyField(source='reviewer.email')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = Review
        fields = ['id', 'listing', 'reviewer', 'reviewer_email', 'listing_title', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['reviewer']