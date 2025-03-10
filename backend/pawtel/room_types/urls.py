from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RoomTypeViewSet

router = DefaultRouter()
router.register(r"", RoomTypeViewSet, basename="room-type")

urlpatterns = [
    path("", include(router.urls)),
]
