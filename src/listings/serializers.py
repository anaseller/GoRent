from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    landlord_email = serializers.ReadOnlyField(source='landlord.email')

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['landlord']

    def validate_address(self, value):
        """
        Проверяет, что адрес не пуст и имеет хотя бы два слова.
        """
        if not value:
            raise serializers.ValidationError("Address cannot be empty.")
        if len(value.split()) < 2:
            raise serializers.ValidationError("Please provide a more specific address.")
        return value.strip().lower()