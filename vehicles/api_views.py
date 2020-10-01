from django.contrib.gis.gdal.geometries import MultiPoint, Point
from django.contrib.gis.geos import GEOSGeometry, Point
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Vehicle, VehicleBrand, Enterprise, Driver, Track
from .serializers import VehicleSerializer, VehicleBrandSerializer, EnterpriseSerializer, DriverSerializer, \
    TrackSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        user = self.request.user
        return Vehicle.objects.filter(
            enterprise__manager=user
        )

    @action(methods=['GET'], detail=True, url_path='tracks')
    def tracks(self, request, pk):
        result = []
        started_at = request.query_params.get('started_at')
        finished_at = request.query_params.get('finished_at')
        tracks = Track.objects.filter(vehicle=pk, started_at__gt=started_at, finished_at__lt=finished_at)

        for track in tracks:
            result.append(track.route)

        return Response(result)


class VehicleBrandViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleBrandSerializer
    queryset = VehicleBrand.objects.all()


class EnterpriseViewSet(viewsets.ModelViewSet):
    serializer_class = EnterpriseSerializer

    def get_queryset(self):
        return Enterprise.objects.filter(
            manager=self.request.user
        )


class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer

    def get_queryset(self):
        return Driver.objects.filter(
            enterprise__manager=self.request.user
        )


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    @action(methods=['POST'], detail=True, url_path='set-point')
    def set_point(self, request, pk):
        track = Track.objects.get(pk=pk)
        mp = GEOSGeometry(track.route)
        lat = request.data.get('lat')
        lon = request.data.get('lon')

        try:
            if lat is None or lon is None:
                raise ValueError('Переданы не валидные координаты')

            point = Point(lat, lon)
            mp.append(point)
            track.route = mp
            track.save()
        except ValueError:
            return Response('Переданы не валидные координаты')

        return Response(point)
