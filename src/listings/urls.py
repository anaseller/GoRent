from django.urls import path, include
from .views import ListingListCreateAPIView, ListingRetrieveUpdateDestroyAPIView, ListingViewsCountAPIView
from src.bookings.views import BookingListCreateAPIView

urlpatterns = [
    path('', ListingListCreateAPIView.as_view(), name='listing-list-create'),
    path('<int:pk>/', ListingRetrieveUpdateDestroyAPIView.as_view(), name='listing-detail'),
    path('<int:listing_pk>/bookings/', BookingListCreateAPIView.as_view(), name='listing-bookings-create'),
    path('views/count/', ListingViewsCountAPIView.as_view(), name='listing-views-count'),
]