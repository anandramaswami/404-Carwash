from django.shortcuts import render
from . models import Services
from . serializers import ServiceSerializers
from rest_framework import viewsets
from .filters import ServiceFilter

# Create your views here.

class Service(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializers
    filterset_class = ServiceFilter