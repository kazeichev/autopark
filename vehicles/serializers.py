from rest_framework import serializers
from .models import Vehicle, VehicleBrand, Enterprise, Driver


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

    class Meta:
        model = Vehicle
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer
    enterprise = EnterpriseSerializer

    class Meta:
        model = Driver
        fields = '__all__'
