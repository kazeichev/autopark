from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Vehicle, VehicleBrand, Enterprise, Driver, Manager, Track, VehicleMileageReport

admin.site.register(Vehicle)
admin.site.register(VehicleBrand)
admin.site.register(Enterprise)
admin.site.register(Driver)
admin.site.register(Manager)
admin.site.register(Track, OSMGeoAdmin)
admin.site.register(VehicleMileageReport)
