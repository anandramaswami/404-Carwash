import django_filters
from .models import Services


class ServiceFilter(django_filters.FilterSet):
    service_name = django_filters.CharFilter(field_name='service_name', lookup_expr='iexact')
    price = django_filters.RangeFilter(field_name='price')

    class Meta:
        model = Services
        fields = ['service_name', 'price']