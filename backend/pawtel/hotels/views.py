from drf_spectacular.utils import extend_schema
from pawtel.bookings.serializers import BookingSerializer
from pawtel.hotels.models import Hotel, HotelImage
from pawtel.hotels.serializers import HotelImageSerializer, HotelSerializer
from pawtel.hotels.services import HotelService
from pawtel.room_types.serializers import RoomTypeSerializer
from pawtel.room_types.services import RoomTypeService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date



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

    @action(
        detail=True,
        methods=["get"],
        url_path="bookings",
        url_name="get_all_bookings_by_hotel",
    )
    def get_all_bookings_by_hotel(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        bookings = HotelService.get_all_bookings_by_hotel(pk)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def __serialize_bookings(bookings):
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(
        detail=False,
        methods=["get"],
        url_path="availables",
        url_name="available_hotels",
    )
    def available_hotels(self, request):
        start_date, end_date = RoomTypeService.parse_availability_dates(request)
        RoomTypeService.validate_room_type_available(start_date, end_date)
        filters = request.query_params.dict()
        hotels = HotelService.list_hotels(filters)
        available_hotels = []
        for hotel in hotels:
            room_types = HotelService.get_all_room_types_of_hotel(hotel.id)
            for room in room_types:
                if RoomTypeService.is_room_type_available(room.id, start_date, end_date):
                    available_hotels.append(hotel)
                    break
        serializer = HotelSerializer(available_hotels, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(
        detail=True,
        methods=["get"],
        url_path="available-room-types",
        url_name="available_room_types",
    )
    def available_room_types(self, request, pk=None):
        start_date, end_date = RoomTypeService.parse_availability_dates(request)
        RoomTypeService.validate_room_type_available(start_date, end_date)
        filters = request.query_params.dict()
        room_types = RoomTypeService.list_availables_room_types_with_filters(pk, filters)
        available_room_types = []
        for room in room_types:
            if RoomTypeService.is_room_type_available(room.id, start_date, end_date):
                available_room_types.append(room)
        serializer = RoomTypeSerializer(available_room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["hotel-images"])
class HotelImageViewSet(viewsets.ViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="hotel-images/upload",
        url_name="upload-image",
    )
    def upload_image(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        input_serializer = HotelService.serialize_input_hotel_image(request, pk)
        HotelService.validate_upload_image(input_serializer, pk)
        hotel_image = HotelService.upload_image_to_hotel(input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            hotel_image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel-images/(?P<image_id>\\d+)",
        url_name="get-image",
    )
    def get_image(self, request, pk=None, image_id=None):
        HotelService.authorize_action_hotel(request, pk)
        hotel_image = HotelService.retrieve_image_from_hotel(pk, image_id)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            hotel_image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel-images/all",
        url_name="get-all-images",
    )
    def get_all_images(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        hotel_images = HotelService.retrieve_all_images_from_hotel(pk)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            hotel_images, many=True, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["put"],
        url_path="hotel-images/(?P<image_id>\\d+)/update",
        url_name="update-image",
    )
    def update_image(self, request, pk=None, image_id=None):
        HotelService.authorize_action_hotel(request, pk)
        input_serializer = HotelService.serialize_input_hotel_image(request, pk)
        HotelService.validate_update_image(input_serializer, pk, image_id)
        hotel_image = HotelService.update_image_to_hotel(input_serializer, pk, image_id)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            hotel_image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
        url_path="hotel-images/(?P<image_id>\\d+)/patch",
        url_name="partial-update-image",
    )
    def partial_update_image(self, request, pk=None, image_id=None):
        return self.update_image(request, pk, image_id)

    @action(
        detail=True,
        methods=["delete"],
        url_path="hotel-images/(?P<image_id>\\d+)/delete",
        url_name="delete-image",
    )
    def delete_image(self, request, pk=None, image_id=None):
        HotelService.authorize_action_hotel(request, pk)
        HotelService.delete_image_from_hotel(pk, image_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel-images/cover",
        url_name="get-cover-image",
    )
    def get_cover_image(self, request, pk=None):
        cover_image = HotelService.retrieve_cover_image(pk)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            cover_image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel-images/non-cover",
        url_name="get-non-cover-images",
    )
    def get_non_cover_images(self, request, pk=None):
        non_cover_images = HotelService.retrieve_all_non_cover_images(pk)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            non_cover_images, many=True, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["put"],
        url_path="hotel-images/(?P<image_id>\\d+)/set-cover",
        url_name="set-image-as-cover",
    )
    def set_image_as_cover(self, request, pk=None, image_id=None):
        HotelService.authorize_action_hotel(request, pk)
        HotelService.validate_set_image_as_cover(pk, image_id)
        cover_image = HotelService.set_image_as_cover(pk, image_id)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            cover_image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)
