from datetime import timedelta
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.room_types.models import RoomType
from pawtel.bookings.models import Booking
from django.db.models import Sum
from pawtel.room_types.serializers import RoomTypeSerializer
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
        HotelOwnerService.get_current_hotel_owner(request)

    @staticmethod
    def serialize_input_room_type_create(request):
        context = {"request": request}
        serializer = RoomTypeSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_create_room_type(request, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")
        hotel = input_serializer.validated_data.get("hotel")
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        if (hotel.is_archived) or (hotel.hotel_owner.id != hotel_owner.id):
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
        
        

    @staticmethod
    def is_room_type_available(room_type_id, start_date, end_date):
        room_type = RoomType.objects.filter(id=room_type_id).first()

        if not room_type:
            raise NotFound("RoomType does not exist.")

        num_rooms = room_type.num_rooms
        max_capacity = num_rooms * room_type.capacity  # Capacidad máxima en cada día

        # Generamos el rango de fechas
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        
        for day in date_range:
            # Contamos el número de reservas activas en ese día
            booked_rooms = Booking.objects.filter(
                room_type=room_type,
                start_date__lte=day,
                end_date__gte=day
            ).count()

            available_capacity = max_capacity - booked_rooms
            if available_capacity <= 0:
                return False  # Si en algún día no hay disponibilidad, retornamos False

        return True
