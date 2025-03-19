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
        filters = request.query_params.dict()  # URL filters checked
        hotels = HotelService.list_hotels(filters)
        output_serializer_data = HotelService.serialize_output_hotel(
            hotels, many=True, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        hotel = HotelService.retrieve_hotel(pk)
        output_serializer_data = HotelService.serialize_output_hotel(
            hotel, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        input_serializer = HotelService.serialize_input_hotel_create(request)
        HotelService.validate_create_hotel(input_serializer)
        hotel_created = HotelService.create_hotel(input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(
            hotel_created, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def upload_image(self, request, pk=None):
        hotel = self.get_object()
        img = HotelService.upload_image_to_hotel(
            hotel, request.data.get("image"), request.data.get("is_cover")
        )
        return Response(img, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        input_serializer = HotelService.serialize_input_hotel_update(request, pk)
        HotelService.validate_update_hotel(pk, input_serializer)
        hotel_updated = HotelService.update_hotel(pk, input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(
            hotel_updated, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

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
        HotelService.authorize_action_hotel(request, pk)
        room_types = HotelService.get_all_room_types_of_hotel(pk)
        serializer = RoomTypeSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
