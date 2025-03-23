from datetime import timedelta

from pawtel.customers.services import CustomerService
from django.utils.dateparse import parse_date
from pawtel.bookings.models import Booking
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError, )


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
    def retrieve_room_type(pk, only_archived=True):
        try:
            return RoomType.objects.get(id=pk)
        except RoomType.DoesNotExist:
            raise NotFound(detail="Room type not found.")

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


    # Availability -----------------------------------------------------------
    
    @staticmethod
    def authorize_room_type_available(request, pk):
        CustomerService.get_current_customer(request)
        room_type = RoomTypeService.retrieve_room_type(pk)

        if (not room_type) or (room_type.is_archived):
            raise NotFound("Room type does not exist.")
    
    @staticmethod
    def parse_availability_dates(request):
        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")

        if not start_date_str or not end_date_str:
            raise ValidationError({"detail": "Both start_date and end_date are required."})

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        
        return start_date, end_date
    
    @staticmethod
    def validate_room_type_available(start_date, end_date):
        if not start_date or not end_date:
            raise ValidationError({"detail": "Invalid date format. Use yyyy-mm-dd."})
        
        if end_date < start_date:
            raise ValidationError({"detail": "End date cannot be earlier than start date."})
    
    @staticmethod
    def is_room_type_available(room_type_id, start_date, end_date):
        """
        Checks if a room type is available for each individual day within the requested date range.
        A room type is available only if, for every day in the range, the number of bookings plus 
        active booking holds does not exceed the total available slots (num_rooms * capacity).
        """
        
        room_type = RoomTypeService.retrieve_room_type(room_type_id)
        total_slots = room_type.num_rooms * room_type.capacity

        days_to_check = [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)  # + 1 because end date is included
        ]

        for day in days_to_check:
            bookings_count = Booking.objects.filter(
                room_type_id=room_type_id,
                start_date__lte=day,  # Booking started before or on this day
                end_date__gte=day      # Booking ends after this day
            ).count()

            if bookings_count >= total_slots:
                return False

        return True

    
    # Filter -----------------------------------------------------------------


    @staticmethod
    def list_availables_room_types_with_filters(hotel_id, filters=None):
        room_types = RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)

        valid_filters = [
            "pet_type",
            "max_price_per_night",
            "min_price_per_night",
            "start_date",
            "end_date",
        ]

        assert filters is None or all(f in valid_filters for f in filters), filters

        if filters:
            if "pet_type" in filters:
                room_types = room_types.filter(pet_type=filters["pet_type"])

            if "max_price_per_night" in filters:
                fl = float(filters["max_price_per_night"])
                assert isinstance(fl, float)
                try:
                    max_price = float(filters["max_price_per_night"])
                    room_types = room_types.filter(
                        price_per_night__lte=max_price
                    ).distinct()
                except ValueError:
                    pass

            if "min_price_per_night" in filters:
                fl = float(filters["min_price_per_night"])
                assert isinstance(fl, float)
                try:
                    min_price = float(filters["min_price_per_night"])
                    room_types = room_types.filter(
                        price_per_night__gte=min_price
                    ).distinct()
                except ValueError:
                    pass

            if "sort_by" in filters:
                assert isinstance(filters["sort_by"], str)

                valid = ["pet_type", "min_price_per_night", "max_price_per_night"]
                assert filters["sort_by"] in valid or filters["sort_by"].startswith("-")

                sort_field = filters["sort_by"]

                if sort_field.startswith("-"):
                    room_types = room_types.order_by(sort_field)
                else:
                    room_types = room_types.order_by(sort_field)

            if "limit" in filters:
                i = int(filters["limit"])
                assert isinstance(i, int)
                try:
                    limit = int(filters["limit"])
                    room_types = room_types[:limit]
                except ValueError:
                    pass

        return room_types