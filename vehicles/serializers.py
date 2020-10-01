from rest_framework import serializers
from .models import Vehicle, VehicleBrand, Enterprise, Driver, Track


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_brand = VehicleBrandSerializer
    enterprise = EnterpriseSerializer
    purchase_date_tz = serializers.ReadOnlyField

    class Meta:
        model = Vehicle
        fields = [
            'enterprise',
            'vehicle_brand',
            'mileage',
            'purchase_date',
            'purchase_date_tz',
            'condition',
            'price',
        ]
        read_only_fields = ['purchase_date_tz']


class DriverSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer
    enterprise = EnterpriseSerializer

    class Meta:
        model = Driver
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer
    route_points = serializers.ReadOnlyField

    class Meta:
        model = Track
        fields = [
            'vehicle',
            'route_points',
            'started_at',
            'finished_at',
            'route'
        ]

