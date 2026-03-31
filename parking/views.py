from django.shortcuts import render
from . models import Parking_Slots
from . serializers import ParkingSerializer
from rest_framework import viewsets
from .filters import ParkingFilter

# Create your views here.

class Parking(viewsets.ModelViewSet):
    queryset = Parking_Slots.objects.all()
    serializer_class = ParkingSerializer
    filterset_class = ParkingFilter
    