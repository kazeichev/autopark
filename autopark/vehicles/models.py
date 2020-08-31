from django.db import models


class Vehicles(models.Model):
    vehicle_brand = models.ForeignKey('VehicleBrands', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)


class VehicleBrands(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    type = models.ForeignKey('VehicleTypes', on_delete=models.CASCADE)
    fuel_type = models.ForeignKey('VehicleFuelTypes', on_delete=models.CASCADE)
    lifting = models.FloatField()
    seats = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)


class VehicleTypes(models.Model):
    TYPE_PASSENGER = 'passenger'
    TYPE_TRUCK = 'truck'
    TYPE_BUS = 'bus'

    TYPES = [
        (TYPE_PASSENGER, 'Легковой автомобиль'),
        (TYPE_TRUCK, 'Грузовой автомобиль'),
        (TYPE_BUS, 'Автобус')
    ]

    type = models.CharField(max_length=20, choices=TYPES, null=False, blank=False)


class VehicleFuelTypes(models.Model):
    TYPE_PETROL = 'petrol'
    TYPE_DIESEL = 'diesel'
    TYPE_GAS = 'gas'

    TYPES = [
        (TYPE_PETROL, 'Бензин'),
        (TYPE_DIESEL, 'Дизель'),
        (TYPE_GAS, 'Газ')
    ]

    type = models.CharField(max_length=20, choices=TYPES, null=False, blank=False)
