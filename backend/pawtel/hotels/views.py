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
        hotels = Hotel.objects.filter(is_archived=False)
        output_serializer_data = HotelService.serialize_output_hotel(hotels, many=True)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        hotel = HotelService.retrieve_hotel(pk)
        output_serializer_data = HotelService.serialize_output_hotel(hotel)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        input_serializer = HotelService.serialize_input_hotel_create(request)
        HotelService.validate_create_hotel(input_serializer)
        hotel_created = HotelService.create_hotel(input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(hotel_created)
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        input_serializer = HotelService.serialize_input_hotel_update(request, pk)
        HotelService.validate_update_hotel(pk, input_serializer)
        hotel_updated = HotelService.update_hotel(pk, input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(hotel_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        return self.update(
            request, pk
        )  # The context of the request specifies that it is PATCH

    def destroy(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        HotelService.delete_hotel(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="room-types",
        url_name="get_all_room_types_of_hotel",
    )
    def get_all_room_types_of_hotel(self, request, pk=None):
        room_types = HotelService.get_all_room_types_of_hotel(pk)
        serializer = RoomTypeSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="room-types/total-vacancy",
        url_name="get_total_vacancy_for_each_room_type_of_hotel",
    )
    def get_total_vacancy_for_each_room_type_of_hotel(self, request, pk=None):
        vacancy_data = HotelService.get_total_vacancy_for_each_room_type_of_hotel(pk)
        return Response(vacancy_data, status=status.HTTP_200_OK)
