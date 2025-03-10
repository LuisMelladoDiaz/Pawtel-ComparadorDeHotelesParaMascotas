from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HotelOwnerViewSet

router = DefaultRouter()
router.register(r"hotel-owners", HotelOwnerViewSet, basename="hotel-owner")

urlpatterns = [
    path("", include(router.urls)),
]
