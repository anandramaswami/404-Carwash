from django.shortcuts import render
from . models import Booking_History
from . serializers import BookingSerializers
from rest_framework import viewsets
from .filters import BookingFilter


# Create your views here.

class Booking(viewsets.ModelViewSet):
    queryset = Booking_History.objects.all()
    serializer_class = BookingSerializers
    filterset_class = BookingFilter


    def update_parking_status(self, booking):
        parking_slot = booking.parking

        if not parking_slot:
            return

        if booking.booking_status in ['Booked', 'Pending']:
            parking_slot.is_available = False
        elif booking.booking_status in ['Completed', 'Cancelled']:
            parking_slot.is_available = True

        parking_slot.save()

    def perform_create(self, serializer):
        booking = serializer.save()
        self.update_parking_status(booking)

    def perform_update(self, serializer):
        booking = serializer.save()
        self.update_parking_status(booking)