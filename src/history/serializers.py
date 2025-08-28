from rest_framework import serializers
from .models import History

class HistorySerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = History
        fields = ['id', 'user_email', 'listing_title', 'action_type', 'timestamp']

class PopularSearchSerializer(serializers.Serializer):
    search_query = serializers.CharField(max_length=255)
    search_count = serializers.IntegerField()