from rest_framework import generics, permissions, status, filters
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from ipware import get_client_ip
from django.utils import timezone
from datetime import timedelta

from .models import Listing
from .serializers import ListingSerializer
from .permissions import IsLandlord
from .filters import ListingFilter
from src.history.models import History
from .serializers import ListingViewsCountSerializer


class ListingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description', 'address']

    ordering_fields = ['price_per_night', 'created_at']

    def get_permissions(self):
        # все могут просматривать
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        # создавать объявления может только арендодатель
        return [IsLandlord()]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем поисковой запрос из параметров url
        search_query = self.request.query_params.get('search', None)

        if search_query:
            # Логируем поисковой запрос
            user = self.request.user if self.request.user.is_authenticated else None
            ip_address, _ = get_client_ip(self.request)

            History.objects.create(
                user=user,
                search_query=search_query,
                action_type='search',
                ip_address=ip_address
            )

            # Применяем фильтр для поиска
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

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


class ListingViewsCountAPIView(generics.ListAPIView):
    """
    Возвращаем список объявлений с количеством просмотров
    """
    serializer_class = ListingViewsCountSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ['views_count']
    ordering = ['-views_count']

    def get_queryset(self):
        user = self.request.user
        queryset = Listing.objects.all()

        # Собираем количество просмотров для каждого объявления
        queryset = queryset.annotate(
            views_count=Count('history', filter=Q(history__action_type='view'))
        )

        # Применяем фильтрацию в зависимости от типа пользователя
        if user.is_landlord:
            # Арендодатель видит только свои объявления
            queryset = queryset.filter(landlord=user)

        return queryset