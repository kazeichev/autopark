from django.contrib import admin

from .models import Vehicle, VehicleBrand, Enterprise, Driver, Manager

admin.site.register(Vehicle)
admin.site.register(VehicleBrand)
admin.site.register(Enterprise)
admin.site.register(Driver)
admin.site.register(Manager)
