from django.db import models

# Create your models here.

class Services(models.Model):
    service_id = models.CharField(max_length=100, unique=True)
    service_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.CharField(max_length=10, default=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name