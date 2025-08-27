from django.urls import path
from .views import HistoryListAPIView

urlpatterns = [
    path('my/', HistoryListAPIView.as_view(), name='history-list'),
]