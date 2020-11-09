from abc import ABC

from django.contrib.gis.geos import Point, GEOSGeometry, MultiPoint, LineString
from django.core.management import BaseCommand
import threading
import random
from vehicles.models import Track, Vehicle


class Command(BaseCommand, ABC):
    help = 'Генерация пути автомобиля'
    time = None
    distance = None
    passed_distance = 0
    vehicle_id = None
    track = None
    max_v = None
    current_point = Point([38.433832, 55.774494])

    def add_arguments(self, parser):
        parser.add_argument('-vid', '--vehicle_id', nargs='?', type=int)
        parser.add_argument('-d', '--distance', nargs='?', type=int)
        parser.add_argument('-t', '--time', nargs='?', type=int)
        parser.add_argument('-mv', '--max_v', nargs='?', type=int)

    def handle(self, *args, **options):
        self.vehicle_id = options['vehicle_id']
        self.distance = options['distance']
        self.time = options['time']
        self.max_v = options['max_v']

        vehicle = Vehicle.objects.get(pk=self.vehicle_id)

        self.track = Track(vehicle=vehicle)
        self.track.route = MultiPoint(self.current_point)
        self.track.save()

        self.drive()

    def drive(self):
        timer = threading.Timer(self.time, self.drive)
        timer.start()

        distance = self.calculate_distance()

        self.passed_distance += distance
        self.current_point = self.create_move_point(distance)
        self.move()

        if self.passed_distance >= self.distance:
            timer.cancel()

    def move(self):
        mp = GEOSGeometry(self.track.route)
        lat = self.current_point[0]
        lon = self.current_point[1]

        point = Point(lat, lon)
        mp.append(point)

        self.track.route = mp
        self.track.save()

    def create_move_point(self, distance):
        lat = self.current_point.coords[0]
        lon = self.current_point.coords[1]
        distance_offset = distance * 1000

        moved_lat = (lat + distance_offset / 111111) + random.random()
        moved_lon = (lon + distance_offset / 111111) + random.random()

        moved_point = LineString(
            self.current_point,
            Point(moved_lat, moved_lon)
        ).interpolate(distance)

        return moved_point

    def calculate_distance(self):
        return self.max_v * self.time
