from rest_framework import serializers
from . models import Parking_Slots


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking_Slots
        fields = '__all__'


class ParkingMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking_Slots
        fields = ['slot_number']