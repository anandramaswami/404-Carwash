import django_filters
from .models import Booking_History
from customers.models import Customers


class BookingFilter(django_filters.FilterSet):
    booking_status = django_filters.CharFilter(field_name='booking_status', lookup_expr='icontains')
    customer = django_filters.ModelChoiceFilter(queryset=Customers.objects.all(), field_name='customer', label='Customer')

    class Meta:
        model = Booking_History
        fields = ['booking_status', 'customer']