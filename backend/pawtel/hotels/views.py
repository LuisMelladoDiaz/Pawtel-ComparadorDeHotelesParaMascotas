import inspect

from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer
from pawtel.hotels.services import HotelService
from pawtel.room_types.serializers import RoomTypeSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def list(self, request):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelService.check_permission(
            request.user, action_name
        )
        filters = request.query_params.dict()  # URL filters checked
        hotels = HotelService.list_hotels(filters, permission_granted, user_type)
        output_serializer_data = HotelService.serialize_output_hotel(hotels, many=True)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelService.check_permission(
            request.user, action_name
        )
        hotel = HotelService.retrieve_hotel(pk, permission_granted, user_type)
        output_serializer_data = HotelService.serialize_output_hotel(hotel)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelService.check_permission(
            request.user, action_name
        )
        input_serializer = HotelService.serialize_input_hotel_create(request)
        HotelService.validate_create_hotel(input_serializer, permission_granted)
        hotel_created = HotelService.create_hotel(input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(hotel_created)
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelService.check_permission(
            request.user, action_name
        )
        HotelService.authorize_action_hotel(request, pk, permission_granted)
        input_serializer = HotelService.serialize_input_hotel_update(
            request, pk, permission_granted
        )
        HotelService.validate_update_hotel(pk, input_serializer)
        hotel_updated = HotelService.update_hotel(
            pk, input_serializer, permission_granted
        )
        output_serializer_data = HotelService.serialize_output_hotel(hotel_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelService.check_permission(
            request.user, action_name
        )
        HotelService.authorize_action_hotel(request, pk, permission_granted)
        HotelService.delete_hotel(pk, permission_granted)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="room-types",
        url_name="get_all_room_types_of_hotel",
    )
    def get_all_room_types_of_hotel(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelService.check_permission(
            request.user, action_name
        )
        HotelService.authorize_action_hotel(request, pk, permission_granted)
        room_types = HotelService.get_all_room_types_of_hotel(pk)
        serializer = RoomTypeSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
