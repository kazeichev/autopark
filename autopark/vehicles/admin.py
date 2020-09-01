from django.contrib import admin

from .models import Vehicle, VehicleBrand

admin.site.register(Vehicle)
admin.site.register(VehicleBrand)