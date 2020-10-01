from django.contrib import admin

from .models import Vehicle, VehicleBrand, Enterprise, Driver, Manager, Track

admin.site.register(Vehicle)
admin.site.register(VehicleBrand)
admin.site.register(Enterprise)
admin.site.register(Driver)
admin.site.register(Manager)
admin.site.register(Track)
