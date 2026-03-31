from django.db import models
from django.conf import settings

# Create your models here.

class Customers(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=10)
    address = models.TextField(max_length=300)
    payment_pin = models.CharField(max_length=4, default='4040')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name
    