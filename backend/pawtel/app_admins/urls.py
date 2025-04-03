from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminViewSet

router = DefaultRouter()
router.register(r"admins", AdminViewSet, basename="admin")

urlpatterns = [
    path("", include(router.urls)),
]
