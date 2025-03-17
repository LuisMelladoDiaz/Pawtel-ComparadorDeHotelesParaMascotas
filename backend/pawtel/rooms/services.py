from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.room_types.services import RoomTypeService
from pawtel.rooms.models import Room
from pawtel.rooms.serializers import RoomSerializer
from rest_framework.exceptions import *


class RoomService:

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_room(request, pk):
        room = RoomService.retrieve_room(pk)
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        if (not room) or (room.is_archived):
            raise NotFound("Room does not exist.")

        if room.room_type.hotel.hotel_owner.id != hotel_owner.id:
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_output_room(room, many=False):
        return RoomSerializer(room, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def list_rooms():
        rooms = Room.objects.filter(is_archived=False)
        return rooms

    @staticmethod
    def retrieve_room(pk):
        return Room.objects.get(id=pk)

    # POST -------------------------------------------------------------------

    @staticmethod
    def authorize_create_room(request):
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        room_type_id = request.data.get("room_type")
        if not room_type_id:
            raise PermissionDenied("Permission denied.")

        room_type = RoomTypeService.retrieve_room_type(room_type_id)

        if not room_type or room_type.hotel.hotel_owner.id != hotel_owner.id:
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_input_room_create(request):
        context = {"request": request}
        serializer = RoomSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_create_room(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")
        room_type = input_serializer.validated_data.get("room_type")
        hotel_id = RoomTypeService.retrieve_room_type(room_type.id).hotel

        if room_type.is_archived:
            raise ValidationError({"room_type": "Invalid room type."})

        if (
            name
            and Room.objects.filter(room_type__hotel_id=hotel_id, name=name).exists()
        ):
            raise ValidationError({"name": "Name in use by same hotel."})

    @staticmethod
    def create_room(input_serializer):
        room_created = input_serializer.save()
        return room_created

    # PUT/PATCH --------------------------------------------------------------

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

        name = input_serializer.validated_data.get("name")
        room_type_id = RoomService.retrieve_room(pk).room_type.id
        hotel_id = RoomTypeService.retrieve_room_type(room_type_id).hotel.id

        if (
            name
            and Room.objects.filter(room_type__hotel_id=hotel_id, name=name).exists()
        ):
            raise ValidationError({"name": "Name in use by same hotel."})

    @staticmethod
    def update_room(pk, input_serializer):
        room = RoomService.retrieve_room(pk)
        return input_serializer.update(room, input_serializer.validated_data)

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_room(pk):
        room = RoomService.retrieve_room(pk)
        room.delete()
