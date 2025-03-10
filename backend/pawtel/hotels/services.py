from django.forms import ValidationError
from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room
from rest_framework.exceptions import NotFound, PermissionDenied


class HotelService:

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_hotel(request, pk):
        hotel = HotelService.retrieve_hotel(pk)

        if not hotel:
            raise NotFound("Hotel does not exist.")

        if hotel.is_archived:
            raise PermissionDenied("")

    @staticmethod
    def serialize_output_hotel(hotel, many=False):
        return HotelSerializer(hotel, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel(pk):
        return Hotel.objects.get(id=pk)

    # POST -------------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_create(request):
        context = {"request": request}
        serializer = HotelSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_create_hotel(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")

        if name and Hotel.objects.filter(name=name).exists():
            raise ValidationError({"username": "Name in use."})

    @staticmethod
    def create_hotel(input_serializer):
        hotel_created = input_serializer.save()
        return hotel_created

    # PUT/PATCH --------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_update(request, pk):
        hotel = HotelService.retrieve_hotel(pk)
        context = {"request": request}
        serializer = HotelSerializer(instance=hotel, data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_update_hotel(pk, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")

        if name and Hotel.objects.filter(name=name).exclude(id=pk).exists():
            raise ValidationError({"username": "Name in use."})

    @staticmethod
    def update_hotel(pk, input_serializer):
        hotel = HotelService.retrieve_hotel(pk)
        return input_serializer.update(hotel, input_serializer.validated_data)

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_hotel(pk):
        hotel = HotelService.retrieve_hotel(pk)
        hotel.delete()

    # OTHERS -----------------------------------------------------------------

    @staticmethod
    def get_all_room_types_of_hotel(hotel_id):
        return RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)

    @staticmethod
    def get_total_vacancy_for_each_room_type_of_hotel(pk):
        room_types = HotelService.get_all_room_types_of_hotel(pk)
        vacancy_data = []

        for room_type in room_types:
            num_rooms = Room.objects.filter(room_type=room_type).count()
            total_vacancy = room_type.capacity * num_rooms
            vacancy_data.append(
                {"room_type_id": room_type.id, "total_vacancy": total_vacancy}
            )

        return vacancy_data
