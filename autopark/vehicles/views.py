# from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Vehicle.objects.filter(
            enterprise__manager=user
        )
