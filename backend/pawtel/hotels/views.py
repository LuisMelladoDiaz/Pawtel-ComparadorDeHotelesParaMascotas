from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer
from pawtel.hotels.services import HotelService
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    @action(detail=True, methods=["get"])
    def get_all_room_types_of_hotel(self, request, pk=None):
        hotel_id = pk
        room_types = HotelService.get_all_room_types_of_hotel(hotel_id)
        return Response(room_types)

    @action(detail=True, methods=["get"])
    def get_total_vacancy_for_each_room_type_of_hotel(self, request, pk=None):
        hotel_id = pk
        vacancy_data = HotelService.get_total_vacancy_for_each_room_type_of_hotel(
            hotel_id
        )
        return Response(vacancy_data)

    def update(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        HotelService.check_if_archived(hotel_owner.id)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        HotelService.check_if_archived(hotel_owner.id)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        HotelService.check_if_archived(hotel_owner.id)
        return super().destroy(request, *args, **kwargs)
