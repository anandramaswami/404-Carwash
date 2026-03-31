import django_filters 
from .models import Customers


class CustomerFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(field_name='customer_name', lookup_expr='icontains')
    id_min = django_filters.CharFilter(method='filter_by_customer_id', label='From Customer ID')
    id_max = django_filters.CharFilter(method='filter_by_customer_id', label='To Customer ID')

    class Meta:
        model = Customers
        fields = ['customer_name', 'id_min', 'id_max']

    def filter_by_customer_id(self, queryset, name, value):
        if name == 'id_min':
            return queryset.filter(customer_id__gte=value)
        elif name == 'id_max':
            return queryset.filter(customer_id__lte=value)
        return queryset
    
