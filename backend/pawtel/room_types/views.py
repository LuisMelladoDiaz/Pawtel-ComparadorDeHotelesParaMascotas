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
        room_types = RoomTypeService.list_room_types()
        output_serializer_data = RoomTypeService.serialize_output_room_type(
            room_types, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        RoomTypeService.authorize_action_room_type(request, pk)
        room_type = RoomTypeService.retrieve_room_type(pk)
        output_serializer_data = RoomTypeService.serialize_output_room_type(room_type)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        RoomTypeService.authorize_create_room_type(request)
        input_serializer = RoomTypeService.serialize_input_room_type_create(request)
        RoomTypeService.validate_create_room_type(request, input_serializer)
        room_type_created = RoomTypeService.create_room_type(input_serializer)
        output_serializer_data = RoomTypeService.serialize_output_room_type(
            room_type_created
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        RoomTypeService.authorize_action_room_type(request, pk)
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
        RoomTypeService.authorize_action_room_type(request, pk)
        RoomTypeService.delete_room_type(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="is-available",
        url_name="is_room_type_available",
    )
    def is_room_type_available(self, request, pk=None):
        RoomTypeService.authorize_room_type_available(request, pk)
        start_date, end_date = RoomTypeService.parse_availability_dates(request)
        RoomTypeService.validate_room_type_available(start_date, end_date)
        is_available = RoomTypeService.is_room_type_available(pk, start_date, end_date)
        return Response({"is_available": is_available}, status=status.HTTP_200_OK)
