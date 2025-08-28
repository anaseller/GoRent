from rest_framework import generics, permissions
from django.db.models import Count
from .models import History
from .serializers import HistorySerializer, PopularSearchSerializer

class HistoryListAPIView(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Return only records associated with the current user
        return History.objects.filter(user=user).select_related('listing')

class PopularSearchAPIView(generics.ListAPIView):
    serializer_class = PopularSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Aggregate search queries by count
        return History.objects.filter(
            action_type='search',
            search_query__isnull=False
        ).values('search_query').annotate(
            search_count=Count('search_query')
        ).order_by('-search_count')[:10]