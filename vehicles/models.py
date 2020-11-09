import json

from django.contrib.gis.geos import GEOSGeometry
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User
import pytz


class Vehicle(models.Model):
    vehicle_brand = models.ForeignKey('VehicleBrand', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mileage = models.FloatField(null=True)
    purchase_date = models.DateTimeField(null=True)
    condition = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE, null=True)

    @property
    def purchase_date_tz(self):
        timezone = pytz.timezone(self.enterprise.timezone)
        return self.purchase_date.astimezone(timezone)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return 'Автомобиль. ID: {}, марка: {}, предприятие {}, цена {}' \
            .format(self.id, self.vehicle_brand.name, self.enterprise.name, self.price)


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


class Enterprise(models.Model):
    timezones = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    name = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    timezone = models.CharField(max_length=255, default='UTC', choices=timezones)

    def __str__(self):
        return self.name


class Driver(models.Model):
    fio = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    salary = models.FloatField()
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return "Водитель {}".format(self.fio)


class Manager(User):
    enterprise = models.ManyToManyField('Enterprise')

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class Track(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    route = gis_models.MultiPointField(null=True)
    started_at = models.DateField(null=False, blank=False)
    finished_at = models.DateField(null=True, default=None, blank=True)

    @property
    def route_points(self):
        return self.route

    def __str__(self):
        return 'Поездка для автомобиля с id {}'.format(self.vehicle.id)


class Report(models.Model):
    TYPE_VEHICLE_MILEAGE = 'vehicle_mileage'

    PERIOD_MONTH = 'month'
    PERIOD_YEAR = 'year'

    TYPES = {
        TYPE_VEHICLE_MILEAGE: 'Пробег автомобиля за период'
    }

    PERIODS = [
        (PERIOD_MONTH, 'Месяц'),
        (PERIOD_YEAR, 'Год')
    ]

    period = models.CharField(max_length=255, choices=PERIODS, null=False, blank=False)
    started_at = models.DateField()
    finished_at = models.DateField()

    class Meta:
        abstract = True

    def get_trans_period(self):
        trans = ''

        if self.period == Report.PERIOD_MONTH:
            trans = 'Месяц'
        elif self.period == Report.PERIOD_YEAR:
            trans = 'Год'

        return trans

    def get_trans_type(self):
        raise NotImplementedError()

    def result(self):
        raise NotImplementedError()


class VehicleMileageReport(Report):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    type = models.CharField(max_length=255,
                            default=Report.TYPE_VEHICLE_MILEAGE,
                            null=False,
                            blank=False,
                            editable=False)

    def result(self):
        result = {}
        format_type = "%Y"
        tracks = Track.objects.filter(
            vehicle=self.vehicle,
            started_at__gt=self.started_at,
            finished_at__lt=self.finished_at
        )

        if self.period == self.PERIOD_MONTH:
            format_type = "%B %Y"

        for track in tracks:
            track_date = track.started_at.strftime(format_type)
            total_distance = 0
            prev_point = None

            for point in track.route:
                if prev_point is None:
                    prev_point = GEOSGeometry(point)
                else:
                    current_point = GEOSGeometry(point)
                    total_distance += prev_point.distance(current_point)

                    prev_point = current_point

            total_distance = round(total_distance) * 100

            if track_date in result:
                result[track_date] += total_distance
            else:
                result[track_date] = total_distance

        return json.dumps(result, ensure_ascii=False)

    def get_trans_type(self):
        return Report.TYPES[self.type]

    def __str__(self):
        return 'Отчёт о пробеге автомобиля с ID {} за {}, с {} по {}' \
            .format(self.vehicle.id, self.get_trans_period(), self.started_at, self.finished_at)
