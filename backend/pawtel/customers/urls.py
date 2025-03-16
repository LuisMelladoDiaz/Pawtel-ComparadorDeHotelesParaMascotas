from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = [
    path("", include(router.urls)),
]
