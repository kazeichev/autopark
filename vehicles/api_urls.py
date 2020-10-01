from rest_framework import routers
from vehicles import api_views

router = routers.SimpleRouter()
router.register('vehicles', api_views.VehicleViewSet, basename='vehicles')
router.register('vehicle-brands', api_views.VehicleBrandViewSet, basename='vehicle-brands')
router.register('enterprises', api_views.EnterpriseViewSet, basename='enterprises')
router.register('drivers', api_views.DriverViewSet, basename='drivers')
router.register('tracks', api_views.TrackViewSet, basename='tracks')

urlpatterns = router.urls
