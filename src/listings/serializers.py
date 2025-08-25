from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    landlord_email = serializers.ReadOnlyField(source='landlord.email')

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['landlord']