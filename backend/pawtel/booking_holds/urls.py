from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingHoldViewSet

router = DefaultRouter()
router.register(r"booking-holds", BookingHoldViewSet, basename="booking-hold")

urlpatterns = [
    path("", include(router.urls)),
]
