from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet

router = DefaultRouter()
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "bookings/hotel/<int:hotel_id>/",
        BookingViewSet.as_view({"get": "list_by_hotel"}),
        name="booking-by-hotel",
    ),
    path(
        "bookings/customer/<int:customer_id>/",
        BookingViewSet.as_view({"get": "list_by_customer"}),
        name="booking-by-customer",
    ),
]
