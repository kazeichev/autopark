from rest_framework import routers
from vehicles import api_views

router = routers.SimpleRouter()
router.register(r'vehicle', api_views.VehicleViewSet, basename='vehicle')
router.register(r'vehicles-brand', api_views.VehicleBrandViewSet, basename='vehicles-brand')
router.register(r'enterprise', api_views.EnterpriseViewSet, basename='enterprise')
router.register(r'driver', api_views.DriverViewSet, basename='driver')

urlpatterns = router.urls
