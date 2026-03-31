from rest_framework import serializers
from . models import Booking_History
from customers.serializers import CustomerMiniSerializers
from parking.serializers import ParkingMiniSerializer
from services.serializers import ServiceMiniSerializers


class BookingSerializers(serializers.ModelSerializer):
    customer = CustomerMiniSerializers(many=False, read_only=True)
    parking = ParkingMiniSerializer(many=False, read_only=True)
    service = ServiceMiniSerializers(many=False, read_only=True)

    class Meta:
        model = Booking_History
        fields = '__all__'

    def validate(self, data):
        parking = data.get('parking')
        status = data.get('booking_status')

        if parking is not None:
            if status in ['Pending', 'Booked'] and not parking.is_available:
                raise serializers.ValidationError("This parking slot is already booked")

        return data