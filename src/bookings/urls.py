from django.urls import path
from .views import BookingListCreateAPIView, BookingConfirmRejectAPIView, BookingCancelAPIView

urlpatterns = [
    path('', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('<int:pk>/confirm/', BookingConfirmRejectAPIView.as_view(), name='booking-confirm-reject'),
    path('<int:pk>/cancel/', BookingCancelAPIView.as_view(), name='booking-cancel'),
]
