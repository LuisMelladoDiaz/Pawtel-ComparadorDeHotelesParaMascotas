from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.services import HotelService
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from pawtel.rooms.models import Room
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class RoomTypeService:

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_room_type(request, pk):
        room_type = RoomTypeService.retrieve_room_type(pk)
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        if (not room_type) or (room_type.is_archived):
            raise NotFound("Room type does not exist.")

        if room_type.hotel.hotel_owner.id != hotel_owner.id:
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_output_room_type(room_type, many=False):
        return RoomTypeSerializer(room_type, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def list_room_types():
        room_types = RoomType.objects.filter(is_archived=False)
        return room_types

    @staticmethod
    def retrieve_room_type(pk):
        return RoomType.objects.get(id=pk)

    # POST -------------------------------------------------------------------

    @staticmethod
    def authorize_create_room_type(request):
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        hotel_id = request.data.get("hotel")
        if not hotel_id:
            raise PermissionDenied("Permission denied.")

        hotel = HotelService.retrieve_hotel(hotel_id)

        if not hotel or hotel.hotel_owner.id != hotel_owner.id:
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_input_room_type_create(request):
        context = {"request": request}
        serializer = RoomTypeSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_create_room_type(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")
        hotel = input_serializer.validated_data.get("hotel")

        if hotel.is_archived:
            raise ValidationError({"hotel": "Invalid hotel."})

        if name and RoomType.objects.filter(hotel_id=hotel.id, name=name).exists():
            raise ValidationError({"name": "Name in use by same hotel."})

    @staticmethod
    def create_room_type(input_serializer):
        room_type_created = input_serializer.save()
        return room_type_created

    # PUT/PATCH --------------------------------------------------------------

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

        name = input_serializer.validated_data.get("name")
        hotel_id = RoomTypeService.retrieve_room_type(pk).hotel.id

        if (
            name
            and RoomType.objects.filter(hotel_id=hotel_id, name=name)
            .exclude(id=pk)
            .exists()
        ):
            raise ValidationError({"name": "Name in use by same hotel."})

    @staticmethod
    def update_room_type(pk, input_serializer):
        room_type = RoomTypeService.retrieve_room_type(pk)
        return input_serializer.update(room_type, input_serializer.validated_data)

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_room_type(pk):
        room_type = RoomType.objects.get(pk=pk)
        room_type.delete()

    # Others -----------------------------------------------------------------

    @staticmethod
    def get_total_vacancy_of_room_type(room_type_id=None):
        total_vacancy = Room.objects.filter(
            room_type_id=room_type_id, is_archived=False
        ).count()
        response_data = {
            "room_type_id": int(room_type_id),
            "total_vacancy": total_vacancy,
        }
        return response_data

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
