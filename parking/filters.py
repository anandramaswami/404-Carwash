import django_filters
from .models import Parking_Slots


class ParkingFilter(django_filters.FilterSet):
    is_available = django_filters.BooleanFilter(field_name='is_available')

    class Meta:
        model = Parking_Slots
        fields = ['is_available']