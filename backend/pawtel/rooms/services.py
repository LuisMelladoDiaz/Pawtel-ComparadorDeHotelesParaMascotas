from django.forms import ValidationError
from pawtel.rooms.models import Room
from pawtel.rooms.serializers import RoomSerializer
from rest_framework.exceptions import NotFound, PermissionDenied


class RoomService:

    @staticmethod
    def authorize_action_room(request, pk):

        room = Room.objects.get(id=pk)

        if not room:
            raise NotFound("Room does not exist.")

        if room.is_archived:
            raise PermissionDenied("")

    @staticmethod
    def retrieve_room(pk):
        return Room.objects.get(pk=pk)

    @staticmethod
    def serialize_input_room_create(request):
        context = {"request": request}
        serializer = RoomSerializer(data=request.data, context=context)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_create_room(input_serializer):
        if not input_serializer.is_valid():
            raise PermissionDenied("Not valid data")
        return True

    @staticmethod
    def create_room(input_serializer):
        room_created = input_serializer.save()
        return room_created

    @staticmethod
    def serialize_output_room(room):
        return RoomSerializer(room).data

    @staticmethod
    def serialize_input_room_update(request, pk):
        context = {"request": request}
        serializer = RoomSerializer(data=request.data, context=context)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_update_room(pk, input_serializer):
        if not input_serializer.is_valid():
            raise PermissionDenied("Not valid data.")
        return True

    @staticmethod
    def update_room(pk, input_serializer):
        room = Room.objects.get(pk=pk)
        return input_serializer.update(room, input_serializer.validated_data)

    @staticmethod
    def serialize_input_room_partial_update(request, pk):
        data = {
            key: value
            for key, value in request.data.items()
            if key
            in RoomSerializer.fields_required_for_post + RoomSerializer.fields_editable
        }
        serializer = RoomSerializer(data=data, partial=True)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_partial_update_room(pk, input_serializer):
        if not input_serializer.is_valid():
            raise PermissionDenied("Not valid data.")
        return True

    @staticmethod
    def partial_update_room(pk, input_serializer):
        room = Room.objects.get(pk=pk)
        return input_serializer.update(room, input_serializer.validated_data)

    @staticmethod
    def delete_room(pk):
        room = Room.objects.get(pk=pk)
        room.delete()
