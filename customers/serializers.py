from rest_framework import serializers
from .models import Customers


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customers 
        fields = '__all__'


class CustomerMiniSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customers 
        fields = ['customer_id', 'customer_name', 'email', 'contact']