from django.db import models
from customers.models import Customers
from parking.models import Parking_Slots
from services.models import Services

# Create your models here.

class Booking_History(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='customer')
    parking = models.ForeignKey(Parking_Slots, on_delete=models.SET_NULL, null=True, related_name='parking')
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service')
    booking_date = models.DateTimeField(auto_now_add=True)
    service_date = models.DateField()
    car_brand = models.CharField(max_length=50, default=True)
    car_model = models.CharField(max_length=50, default=True)
    car_color = models.CharField(max_length=30, default=True)
    car_reg_num = models.CharField(max_length=20, default=True)
    booking_status = models.CharField(max_length=30, choices=[('Pending', 'Pending'), ('Booked', 'Booked'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending')
    payment_status = models.CharField(max_length=30, choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], default='Unpaid')
    payment_id = models.CharField(max_length=100, blank=True, null=True)

from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=Booking_History)
def release_parking_slot(sender, instance, **kwargs):
    if instance.parking:
        instance.parking.is_available = True
        instance.parking.save()
