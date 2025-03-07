from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.serializers import HotelSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class HotelOwnerViewSet(viewsets.ModelViewSet):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerSerializer

    def update(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        HotelOwnerService.check_if_active(hotel_owner.id)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        HotelOwnerService.check_if_active(hotel_owner.id)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        HotelOwnerService.check_if_active(hotel_owner.id)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def get_all_hotels_of_hotel_owner(self, request, pk=None):
        hotel_owner = self.get_object()
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(hotel_owner.id)
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["delete"])
    def delete_all_hotels_of_hotel_owner(self, request, pk=None):
        hotel_owner = self.get_object()
        hotels_deleted = HotelOwnerService.delete_all_hotels_of_hotel_owner(
            hotel_owner.id
        )
        return Response(
            {"message": f"{hotels_deleted} hoteles eliminados."},
            status=status.HTTP_204_NO_CONTENT,
        )
