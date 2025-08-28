from django.urls import path
from .views import HistoryListAPIView, PopularSearchAPIView

urlpatterns = [
    path('my/', HistoryListAPIView.as_view(), name='history-list'),
    path('popular/', PopularSearchAPIView.as_view(), name='popular-searches'),
]