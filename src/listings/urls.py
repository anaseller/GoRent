from django.urls import path
from .views import ListingListCreateAPIView, ListingRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('listings/', ListingListCreateAPIView.as_view(), name='listing-list-create'),
    path('listings/<int:pk>/', ListingRetrieveUpdateDestroyAPIView.as_view(), name='listing-detail'),
]