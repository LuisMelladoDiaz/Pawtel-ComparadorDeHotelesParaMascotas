from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HotelImageViewSet, HotelViewSet

router = DefaultRouter()
router.register(r"hotels", HotelViewSet, basename="hotel")
router.register(r"hotels", HotelImageViewSet, basename="hotel-image")

urlpatterns = [
    path("", include(router.urls)),
]
