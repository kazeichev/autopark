from rest_framework import serializers
from .models import Vehicle, VehicleBrand, Enterprise


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = [
            'name',
            'city',
        ]


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = [
            'name',
            'type',
            'fuel_type',
            'lifting',
            'seats',
            'created_at',
            'updated_at',
        ]


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_brand = VehicleBrandSerializer()
    enterprise = EnterpriseSerializer()

    class Meta:
        model = Vehicle
        fields = [
            'vehicle_brand',
            'mileage',
            'purchase_date',
            'condition',
            'price',
            'enterprise',
            'created_at',
            'updated_at'
        ]
