from rest_framework import serializers
from . models import Services


class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


class ServiceMiniSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['service_name', 'description', 'price', 'duration_minutes']