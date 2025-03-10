from django.forms import ValidationError
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from pawtel.rooms.models import Room
from rest_framework.exceptions import NotFound, PermissionDenied


class RoomTypeService:

    @staticmethod
    def list_room_types():
        room_types = RoomType.objects.filter(is_archived=False)
        return room_types

    @staticmethod
    def authorize_action_room_type(request, pk):

        room_type = RoomTypeService.retrieve_room_type(pk)
        if not room_type:
            raise NotFound("This type of room does not exist.")
        if room_type.is_archived:
            raise PermissionDenied("")

    @staticmethod
    def serialize_output_room_type(room_type, many=False):
        return RoomTypeSerializer(room_type, many=many).data

    @staticmethod
    def retrieve_room_type(pk):
        return RoomType.objects.get(id=pk)

    @staticmethod
    def serialize_input_room_type_create(request):
        context = {"request": request}
        serializer = RoomTypeSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_create_room_type(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)
        return True

    @staticmethod
    def create_room_type(input_serializer):
        room_type_created = input_serializer.save()
        return room_type_created

    @staticmethod
    def serialize_input_room_type_update(request, pk):
        room_type = RoomTypeService.retrieve_room_type(pk)
        context = {"request": request}
        serializer = RoomTypeSerializer(
            instance=room_type, data=request.data, context=context
        )
        return serializer

    @staticmethod
    def validate_update_room_type(pk, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)
        return True

    @staticmethod
    def update_room_type(pk, input_serializer):
        room_type = RoomTypeService.retrieve_room_type(pk)
        return input_serializer.update(room_type, input_serializer.validated_data)

    @staticmethod
    def delete_room_type(pk):
        room_type = RoomType.objects.get(pk=pk)
        room_type.delete()

    @staticmethod
    def get_total_vacancy_of_room_type(room_type_id=None):
        total_vacancy = Room.objects.filter(
            room_type_id=room_type_id, is_archived=False
        ).count()
        return total_vacancy

    @staticmethod
    def get_all_rooms_of_room_type(room_type_id=None):
        rooms = Room.objects.filter(room_type_id=room_type_id, is_archived=False)
        return rooms

    @staticmethod
    def get_vacancy_for_each_room_of_room_type(room_type_id=None):
        rooms = RoomTypeService.get_all_rooms_of_room_type(room_type_id)
        vacancy_list = []
        for room in rooms:
            vacancy_list.append(
                {"room_id": room.id, "vacancy": room.room_type.capacity}
            )
        return vacancy_list
