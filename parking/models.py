from django.db import models

# Create your models here.

class Parking_Slots(models.Model):
    slot_number = models.CharField(max_length=100, unique=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slot_number