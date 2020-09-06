from rest_framework import viewsets
from .models import Vehicle, VehicleBrand, Enterprise, Driver
from .serializers import VehicleSerializer, VehicleBrandSerializer, EnterpriseSerializer, DriverSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        user = self.request.user
        return Vehicle.objects.filter(
            enterprise__manager=user
        )


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
