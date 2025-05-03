from inspect import currentframe

from drf_spectacular.utils import extend_schema
from pawtel.app_admins.services import AdminService
from pawtel.bookings.serializers import BookingSerializer
from pawtel.hotels.models import Hotel, HotelImage
from pawtel.hotels.serializers import HotelImageSerializer, HotelSerializer
from pawtel.hotels.services import HotelService
from pawtel.room_types.serializers import RoomTypeSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# -
# -------------------------------------------------------------------------
# Hotels ------------------------------------------------------------------
# -------------------------------------------------------------------------
# -


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def list(self, request):
        filters = request.query_params.dict()
        is_admin = AdminService.is_current_user_admin(request)
        hotels = HotelService.list_filtered_hotels(filters, allow_archived=is_admin)
        serializer = HotelSerializer(hotels, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        is_admin = AdminService.is_current_user_admin(request)
        hotel = HotelService.retrieve_hotel(pk, allow_archived=is_admin)
        output_serializer_data = HotelService.serialize_output_hotel(
            hotel, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name)
        input_serializer = HotelService.serialize_input_hotel_create(request)
        HotelService.validate_create_hotel(input_serializer)
        hotel_created = HotelService.create_hotel(input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(hotel_created)
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        input_serializer = HotelService.serialize_input_hotel_update(request, pk)
        HotelService.validate_update_hotel(pk, input_serializer)
        hotel_updated = HotelService.update_hotel(pk, input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(hotel_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        delete = HotelService.validate_all_room_types_deletion(pk)
        if delete:
            HotelService.delete_hotel(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            HotelService.archive_hotel(pk)
            return Response(
                {"detail": "Hotel archivado en vez de eliminado por reservas pasadas."},
                status=status.HTTP_200_OK,
            )

    @action(
        detail=True,
        methods=["get"],
        url_path="room-types",
        url_name="list_room_types_of_hotel",
    )
    def list_room_types_of_hotel(self, request, pk=None):
        room_types = HotelService.list_room_types_of_hotel(pk)
        serializer = RoomTypeSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="bookings",
        url_name="list_bookings_of_hotel",
    )
    def list_bookings_of_hotel(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        bookings = HotelService.list_bookings_of_hotel(pk)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -
# -------------------------------------------------------------------------
# HotelImages -------------------------------------------------------------
# -------------------------------------------------------------------------
# -


@extend_schema(tags=["hotel-images"])
class HotelImageViewSet(viewsets.ViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel-images/all",
        url_name="list_images_of_hotel",
    )
    def list_images_of_hotel(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        hotel_images = HotelService.list_images_of_hotel(pk)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            hotel_images, many=True, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel-images/(?P<image_id>\\d+)",
        url_name="get-image",
    )
    def retrieve_image(self, request, pk=None, image_id=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        hotel_image = HotelService.retrieve_image_from_hotel(pk, image_id)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            hotel_image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path="hotel-images/upload",
        url_name="upload-image",
    )
    def upload_image(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        input_serializer = HotelService.serialize_input_hotel_image(request, pk)
        HotelService.validate_upload_image(input_serializer, pk)
        hotel_image = HotelService.upload_image_to_hotel(input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            hotel_image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["put"],
        url_path="hotel-images/(?P<image_id>\\d+)/update",
        url_name="update-image",
    )
    def update_image(self, request, pk=None, image_id=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
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
        # The context of the request specifies that it is PATCH
        return self.update_image(request, pk, image_id)

    @action(
        detail=True,
        methods=["delete"],
        url_path="hotel-images/(?P<image_id>\\d+)/delete",
        url_name="delete-image",
    )
    def destroy_image(self, request, pk=None, image_id=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        HotelService.delete_image_from_hotel(pk, image_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel-images/cover",
        url_name="get-cover-image",
    )
    def get_cover_image(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk)
        cover_image = HotelService.retrieve_current_cover_image_or_404(pk)
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
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk)
        non_cover_images = HotelService.list_non_cover_images(pk)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            non_cover_images, many=True, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["put"],
        url_path="hotel-images/(?P<image_id>\\d+)/set-is-cover",
        url_name="set-image-is-cover",
    )
    def set_image_is_cover(self, request, pk=None, image_id=None):
        action_name = currentframe().f_code.co_name
        HotelService.authorize_action_hotel(request, action_name, pk, True)
        input_serializer = HotelService.serialize_input_set_image_is_cover(request)
        HotelService.validate_set_image_is_cover(input_serializer)
        image = HotelService.set_image_is_cover(input_serializer, pk, image_id)
        output_serializer_data = HotelService.serialize_output_hotel_image(
            image, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)
