"""autopark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.contrib.auth import views as auth_views

from vehicles.api_views import VehicleViewSet, VehicleBrandViewSet, EnterpriseViewSet, DriverViewSet
from vehicles.views import manager, vehicle_edit, enterprise_view, vehicle_view, vehicle_delete, vehicle_create

router = routers.SimpleRouter()
router.register(r'vehicles', VehicleViewSet, basename='VehicleView')
router.register(r'vehicles-brand', VehicleBrandViewSet, basename='VehicleBrandView')
router.register(r'enterprise', EnterpriseViewSet, basename='EnterpriseView')
router.register(r'drivers', DriverViewSet, basename='DriverView')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('enterprise/<int:enterprise_id>/', enterprise_view, name='enterprise-view'),
    path('enterprise/<int:enterprise_id>/vehicle/create/', vehicle_create, name='vehicle-create'),
    path('enterprise/<int:enterprise_id>/vehicle/<int:vehicle_id>/', vehicle_view, name='vehicle-view'),
    path('enterprise/<int:enterprise_id>/vehicle/<int:vehicle_id>/edit/', vehicle_edit, name='vehicle-edit'),
    path('enterprise/<int:enterprise_id>/vehicle/<int:vehicle_id>/delete/', vehicle_delete, name='vehicle-delete'),
    path('', manager)
]
