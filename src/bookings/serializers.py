from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.email')

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'check_in_date', 'check_out_date', 'status', 'created_at',
                  'updated_at']
        read_only_fields = ['tenant']