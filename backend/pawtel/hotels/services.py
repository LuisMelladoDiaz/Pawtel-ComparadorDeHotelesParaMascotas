from django.forms import ValidationError
from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room
from rest_framework.exceptions import NotFound, PermissionDenied


class HotelService:

    @staticmethod
    def authorize_action_hotel(request, pk):

        hotel = Hotel.objects.get(id=pk)

        if not hotel:
            raise NotFound("Hotel owner does not exist.")

        if hotel.is_archived:
            raise PermissionDenied("")

    @staticmethod
    def retrieve_hotel(pk):
        return Hotel.objects.get(pk=pk)

    @staticmethod
    def serialize_input_hotel_create(request):
        serializer = HotelSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_create_hotel(input_serializer):
        if not input_serializer.is_valid():
            raise PermissionDenied("Not valid data")
        return True

    @staticmethod
    def create_hotel(input_serializer):
        hotel_created = input_serializer.save()
        return hotel_created

    @staticmethod
    def serialize_output_hotel(hotel):
        return HotelSerializer(hotel).data

    @staticmethod
    def serialize_input_hotel_update(request, pk):
        data = {
            key: value
            for key, value in request.data.items()
            if key
            in HotelSerializer.fields_required_for_post
            + HotelSerializer.fields_editable
        }
        serializer = HotelSerializer(data=data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_update_hotel(pk, input_serializer):
        if not input_serializer.is_valid():
            raise PermissionDenied("Not valid data.")
        return True

    @staticmethod
    def update_hotel(pk, input_serializer):
        hotel = Hotel.objects.get(pk=pk)
        return input_serializer.update(hotel, input_serializer.validated_data)

    @staticmethod
    def serialize_input_hotel_partial_update(request, pk):
        data = {
            key: value
            for key, value in request.data.items()
            if key
            in HotelSerializer.fields_required_for_post
            + HotelSerializer.fields_editable
        }
        serializer = HotelSerializer(data=data, partial=True)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_partial_update_hotel(pk, input_serializer):
        if not input_serializer.is_valid():
            raise PermissionDenied("dos para la actualización parcial del hotel.")
        return True

    @staticmethod
    def partial_update_hotel(pk, input_serializer):
        hotel = Hotel.objects.get(pk=pk)
        return input_serializer.update(hotel, input_serializer.validated_data)

    @staticmethod
    def delete_hotel(pk):
        hotel = Hotel.objects.get(pk=pk)
        hotel.delete()

    @staticmethod
    def get_all_room_types_of_hotel(request, pk):
        hotel = Hotel.objects.get(pk=pk)
        return RoomType.objects.filter(hotel=hotel)

    @staticmethod
    def get_total_vacancy_for_each_room_type_of_hotel(request, pk):
        hotel = Hotel.objects.get(pk=pk)
        room_types = RoomType.objects.filter(hotel=hotel)

        vacancy_data = []

        for room_type in room_types:
            rooms = Room.objects.filter(room_type=room_type).count()
            total_vacancy = room_type.capacity * rooms
            vacancy_data.append(
                {"room_type_id": room_type.id, "total_vacancy": total_vacancy}
            )

        return vacancy_data
