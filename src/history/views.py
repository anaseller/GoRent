from rest_framework import generics, permissions
from .models import History
from .serializers import HistorySerializer

class HistoryListAPIView(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Возвращаем только записи, связанные с текущим пользователем
        return History.objects.filter(user=user).select_related('listing')