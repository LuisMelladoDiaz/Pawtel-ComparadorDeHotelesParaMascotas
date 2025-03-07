from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HotelViewSet

router = DefaultRouter()
router.register(r"hotels", HotelViewSet, basename="hotel")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "hotels/<int:pk>/room-types/",
        HotelViewSet.as_view({"get": "get_all_room_types_of_hotel"}),
        name="get_all_room_types_of_hotel",
    ),
    path(
        "hotels/<int:pk>/room-types/total-vacancy",
        HotelViewSet.as_view({"get": "get_total_vacancy_for_each_room_type_of_hotel"}),
        name="get_total_vacancy_for_each_room_type_of_hotel",
    ),
]
