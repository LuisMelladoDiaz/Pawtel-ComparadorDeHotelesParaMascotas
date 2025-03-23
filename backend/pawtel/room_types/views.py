import inspect

from pawtel.hotels.services import HotelService
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from pawtel.room_types.services import RoomTypeService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def list(self, request):
        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_1(request, action_name)
        room_types = RoomTypeService.list_room_types()
        output_serializer_data = RoomTypeService.serialize_output_room_type(
            room_types, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_2(request, pk, action_name)
        room_type = RoomTypeService.retrieve_room_type(pk)
        output_serializer_data = RoomTypeService.serialize_output_room_type(room_type)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_1(request, action_name)
        input_serializer = RoomTypeService.serialize_input_room_type_create(request)
        RoomTypeService.validate_create_room_type(request, input_serializer)
        room_type_created = RoomTypeService.create_room_type(input_serializer)
        output_serializer_data = RoomTypeService.serialize_output_room_type(
            room_type_created
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_3(request, pk, action_name)
        input_serializer = RoomTypeService.serialize_input_room_type_update(request, pk)
        RoomTypeService.validate_update_room_type(pk, input_serializer)
        room_type_updated = RoomTypeService.update_room_type(pk, input_serializer)
        output_serializer_data = RoomTypeService.serialize_output_room_type(
            room_type_updated
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_3(request, pk, action_name)
        RoomTypeService.delete_room_type(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        today = date.today()
        past_limit = today - timedelta(days=1096)

        past_bookings = Booking.objects.filter(
            room_type_id=pk, start_date__range=(past_limit, today)
        )
        future_bookings = Booking.objects.filter(room_type_id=pk, start_date__gte=today)

        if future_bookings.exists():
            raise ValidationError(
                "Cannot delete room type because there is an upcoming booking."
            )

        if past_bookings.exists():
            RoomType.objects.filter(pk=pk).update(is_archived=True)
        raise ValidationError(
            "Cannot delete room type because there are bookings in the past 3 years. The room type has been archived instead."
        )

        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_3(request, pk, action_name)
        RoomTypeService.delete_room_type(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="is-available",
        url_name="is_room_type_available",
    )
    def is_room_type_available(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_2(request, pk, action_name)
        start_date, end_date = RoomTypeService.parse_availability_dates(request)
        RoomTypeService.validate_room_type_available(start_date, end_date)
        is_available = RoomTypeService.is_room_type_available(pk, start_date, end_date)
        return Response({"is_available": is_available}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotel",
        url_name="get_hotel_of_room_type",
    )
    def get_hotel_of_room_type(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        RoomTypeService.authorize_action_room_type_level_2(request, pk, action_name)
        hotel = RoomTypeService.get_hotel_of_room_type(pk)
        output_serializer_data = HotelService.serialize_output_hotel(
            hotel, context={"request": request}
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)
