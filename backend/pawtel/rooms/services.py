from django.forms import ValidationError
from pawtel.rooms.models import Room
from pawtel.rooms.serializers import RoomSerializer
from rest_framework.exceptions import NotFound, PermissionDenied


class RoomService:

    @staticmethod
    def authorize_action_room(request, pk):

        room = RoomService.retrieve_room(pk)
        if not room:
            raise NotFound("Room does not exist.")

        if room.is_archived:
            raise PermissionDenied("")

    @staticmethod
    def serialize_output_room(room, many=False):
        return RoomSerializer(room, many=many).data

    @staticmethod
    def retrieve_room(pk):
        return Room.objects.get(id=pk)

    @staticmethod
    def serialize_input_room_create(request):
        context = {"request": request}
        serializer = RoomSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_create_room(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)
        return True

    @staticmethod
    def create_room(input_serializer):
        room_created = input_serializer.save()
        return room_created

    @staticmethod
    def serialize_input_room_update(request, pk):
        room = RoomService.retrieve_room(pk)
        context = {"request": request}
        serializer = RoomSerializer(instance=room, data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_update_room(pk, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)
        return True

    @staticmethod
    def update_room(pk, input_serializer):
        room = RoomService.retrieve_room(pk)
        return input_serializer.update(room, input_serializer.validated_data)

    @staticmethod
    def delete_room(pk):
        room = RoomService.retrieve_room(pk)
        room.delete()
