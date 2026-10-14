from rest_framework import serializers
from .models import Booking, BookingPayment
from vehicles.serializers import VehicleSerializer, CitySerializer
from users.serializers import UserSerializer


class BookingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.IntegerField(write_only=True)
    destination_city = CitySerializer(read_only=True)
    destination_city_id = serializers.IntegerField(write_only=True, required=False)
    user = UserSerializer(read_only=True)
    payment = BookingPaymentSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'vehicle', 'vehicle_id', 'booking_type', 'pickup_date',
            'return_date', 'destination_city', 'destination_city_id', 'departure_date',
            'return_date_intercity', 'pickup_location', 'total_amount', 'status',
            'special_requests', 'created_at', 'payment'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'payment']


class BookingCreateSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.IntegerField()
    destination_city_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Booking
        fields = [
            'vehicle_id', 'booking_type', 'pickup_date', 'return_date',
            'destination_city_id', 'departure_date', 'return_date_intercity',
            'pickup_location', 'special_requests'
        ]

    def validate(self, data):
        if data['booking_type'] == 'intercity':
            if not data.get('destination_city_id'):
                raise serializers.ValidationError("Destination city is required for intercity trips.")
            if not data.get('departure_date'):
                raise serializers.ValidationError("Departure date is required for intercity trips.")
        else:
            if not data.get('pickup_date') or not data.get('return_date'):
                raise serializers.ValidationError("Pickup and return dates are required for local rentals.")
        
        return data


class BookingListSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    destination_city = CitySerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'vehicle', 'booking_type', 'pickup_date', 'return_date',
            'destination_city', 'status', 'total_amount', 'created_at'
        ]
