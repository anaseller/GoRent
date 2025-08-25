import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    price_per_night = django_filters.RangeFilter()
    num_rooms = django_filters.RangeFilter()

    class Meta:
        model = Listing
        fields = {
            'address': ['exact', 'icontains'],
            'housing_type': ['exact'],
        }