from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from pawtel.room_types.services import RoomTypeService
from pawtel.rooms.serializers import RoomSerializer
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
        RoomTypeService.validate_create_room_type(input_serializer)
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
        url_path="total-vacancy",
        url_name="get_total_vacancy_of_room_type",
    )
    def get_total_vacancy_of_room_type(self, request, pk=None):
        RoomTypeService.authorize_action_room_type(request, pk)
        total_vacancy_data = RoomTypeService.get_total_vacancy_of_room_type(pk)
        return Response(total_vacancy_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="rooms",
        url_name="get_all_rooms_of_room_type",
    )
    def get_all_rooms_of_room_type(self, request, pk=None):
        RoomTypeService.authorize_action_room_type(request, pk)
        rooms = RoomTypeService.get_all_rooms_of_room_type(pk)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="rooms/vacancy",
        url_name="get_vacancy_for_each_room_of_room_type",
    )
    def get_vacancy_for_each_room_of_room_type(self, request, pk=None):
        RoomTypeService.authorize_action_room_type(request, pk)
        vacancy_list = RoomTypeService.get_vacancy_for_each_room_of_room_type(pk)
        return Response(vacancy_list, status=status.HTTP_200_OK)
