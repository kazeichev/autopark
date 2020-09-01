from django.contrib import admin

from .models import Vehicle, VehicleBrand, Enterprise, Driver

admin.site.register(Vehicle)
admin.site.register(VehicleBrand)
admin.site.register(Enterprise)
admin.site.register(Driver)
