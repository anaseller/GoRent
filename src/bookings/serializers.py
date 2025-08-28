from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    tenant_email = serializers.ReadOnlyField(source='tenant.email')

    listing_id = serializers.ReadOnlyField(source='listing.id')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = Booking
        fields = [
            'id', 'tenant_email', 'listing_id', 'listing_title',
            'check_in_date', 'check_out_date', 'status', 'created_at', 'updated_at'
        ]