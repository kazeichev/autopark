from abc import ABC
import random

from django.core.management import BaseCommand
from randomtimestamp import randomtimestamp

from vehicles.models import Enterprise, Vehicle, VehicleBrand


class Command(BaseCommand, ABC):
    help = 'Генерация фейковых машин для заданных предприятий'

    def add_arguments(self, parser):
        parser.add_argument('vehicles_count', nargs='?', type=int)
        parser.add_argument('enterprise_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        enterprise_ids = options['enterprise_ids']
        vehicles_count = options['vehicles_count']

        self.stdout.write(
            self.style.WARNING(
                'Начинаю создание автомобилей для компаний с ids {}'.format(enterprise_ids)
            )
        )

        for enterprise_id in enterprise_ids:
            enterprise = Enterprise.objects.filter(id=enterprise_id).first()

            for i in range(vehicles_count):
                vehicle_brand = VehicleBrand.objects.filter(id=random.randrange(1, 5)).first()

                vehicle = Vehicle(
                    enterprise=enterprise,
                    vehicle_brand=vehicle_brand,
                    mileage=random.randrange(1, 400000),
                    purchase_date=randomtimestamp(start_year=1994, text=False).strftime("%Y-%m-%d %H:%M:%S"),
                    condition=random.randrange(0, 5),
                    price=random.randrange(1, 1000000)
                )

                vehicle.save()

        self.stdout.write(self.style.SUCCESS('Автомобили успешно созданы'))
