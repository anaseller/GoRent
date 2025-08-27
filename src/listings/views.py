from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from ipware import get_client_ip
from django.utils import timezone
from datetime import timedelta

from .models import Listing
from .serializers import ListingSerializer
from .permissions import IsLandlord
from .filters import ListingFilter
from src.history.models import History



class ListingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description', 'address']

    def get_permissions(self):
        # все могут просматривать
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        # создавать объявления может только арендодатель
        return [IsLandlord()]

    def perform_create(self, serializer):
        """
        Автоматически заполняет поле landlord текущим авторизованным пользователем
        """
        serializer.save(landlord=self.request.user)


class ListingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_permissions(self):
        """
        Устанавливает права доступа в зависимости от метода запроса.
        """
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [IsLandlord()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user if request.user.is_authenticated else None
        ip_address, _ = get_client_ip(request)

        # Защита от накрутки: не записываем просмотр, если он уже был в последние 30 минут с того же IP/пользователя
        threshold = timezone.now() - timedelta(minutes=30)

        if user:
            last_view = History.objects.filter(user=user, listing=instance, action_type='view').order_by(
                '-timestamp').first()
            if not last_view or last_view.timestamp < threshold:
                History.objects.create(user=user, listing=instance, action_type='view', ip_address=ip_address)
        else:
            last_view = History.objects.filter(ip_address=ip_address, listing=instance, action_type='view').order_by(
                '-timestamp').first()
            if not last_view or last_view.timestamp < threshold:
                History.objects.create(listing=instance, action_type='view', ip_address=ip_address)

        return super().retrieve(request, *args, **kwargs)