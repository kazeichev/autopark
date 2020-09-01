from django.db import models


class Vehicle(models.Model):
    vehicle_brand = models.ForeignKey('VehicleBrand', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mileage = models.FloatField(null=True)
    purchase_date = models.DateTimeField(null=True)
    condition = models.IntegerField(null=True)

    def __str__(self):
        return self.vehicle_brand.name


class VehicleBrand(models.Model):
    VEHICLE_TYPE_PASSENGER = 'passenger'
    VEHICLE_TYPE_TRUCK = 'truck'
    VEHICLE_TYPE_BUS = 'bus'

    VEHICLE_TYPES = [
        (VEHICLE_TYPE_PASSENGER, 'Легковой автомобиль'),
        (VEHICLE_TYPE_TRUCK, 'Грузовой автомобиль'),
        (VEHICLE_TYPE_BUS, 'Автобус')
    ]

    FUEL_TYPE_PETROL = 'petrol'
    FUEL_TYPE_DIESEL = 'diesel'
    FUEL_TYPE_GAS = 'gas'

    FUEL_TYPES = [
        (FUEL_TYPE_PETROL, 'Бензин'),
        (FUEL_TYPE_DIESEL, 'Дизель'),
        (FUEL_TYPE_GAS, 'Газ')
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(max_length=20, choices=VEHICLE_TYPES, null=False, blank=False)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, null=False, blank=False)
    lifting = models.FloatField()
    seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
