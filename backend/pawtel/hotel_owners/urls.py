from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HotelOwnerViewSet

router = DefaultRouter()
router.register(r"hotel-owners", HotelOwnerViewSet, basename="hotel-owner")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "hotel-owners/<int:hotel_owner_id>/hotels/",
        HotelOwnerViewSet.as_view(
            {
                "get": "get_all_hotels_of_hotel_owner",
                "delete": "delete_all_hotels_of_hotel_owner",
            }
        ),
        name="hotel-owner-hotels",
    ),
]
