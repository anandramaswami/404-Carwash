from django.shortcuts import render
from rest_framework import viewsets
from .models import Customers
from .serializers import CustomerSerializers
from .filters import CustomerFilter


# Create your views here.

class Customer(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializers
    filterset_class = CustomerFilter