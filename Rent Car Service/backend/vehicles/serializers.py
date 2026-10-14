from rest_framework import serializers
from .models import Vehicle, VehicleCategory, City


class VehicleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    category = VehicleCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'name', 'brand', 'model_year', 'category', 'category_id',
            'fuel_type', 'transmission', 'seats', 'daily_rate', 'weekly_rate',
            'monthly_rate', 'image', 'description', 'features', 'is_available',
            'mileage', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class VehicleListSerializer(serializers.ModelSerializer):
    category = VehicleCategorySerializer(read_only=True)
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'name', 'brand', 'model_year', 'category', 'fuel_type',
            'transmission', 'seats', 'daily_rate', 'image', 'is_available'
        ]
