from datetime import timedelta

from django.utils.dateparse import parse_date
from django.utils.timezone import now
from pawtel.app_users.services import AppUserService
from pawtel.booking_holds.models import BookingHold
from pawtel.bookings.services import BookingService
from pawtel.customers.services import CustomerService
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class RoomTypeService:

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_room_type(request, pk):
        room_type = RoomTypeService.retrieve_room_type(pk)
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        if room_type.hotel.hotel_owner.id != hotel_owner.id:
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_output_room_type(room_type, many=False):
        return RoomTypeSerializer(room_type, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def list_room_types(allow_archived=False):
        if allow_archived:
            return RoomType.objects.all()
        else:
            return RoomType.objects.filter(is_archived=False)

    @staticmethod
    def retrieve_room_type(pk, allow_archived=False):
        try:
            if allow_archived:
                return RoomType.objects.get(id=pk)
            else:
                return RoomType.objects.get(id=pk, is_archived=False)
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

        if hotel.hotel_owner.id != hotel_owner.id:
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
        RoomTypeService.retrieve_room_type(pk)

    @staticmethod
    def parse_availability_dates(request):
        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")

        if not start_date_str or not end_date_str:
            raise ValidationError(
                {"detail": "Both start_date and end_date are required."}
            )

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        return start_date, end_date

    @staticmethod
    def validate_room_type_available(start_date, end_date):
        if not start_date or not end_date:
            raise ValidationError({"detail": "Invalid date format. Use yyyy-mm-dd."})

        if end_date < start_date:
            raise ValidationError(
                {"detail": "End date cannot be earlier than start date."}
            )

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
            for i in range(
                (end_date - start_date).days + 1
            )  # + 1 because end date is included
        ]

        for day in days_to_check:
            bookings_count = BookingService.count_bookings_of_room_type_at_date(
                room_type_id, day
            )

            # Cannot call function due to circular dependency
            active_booking_holds_count = BookingHold.objects.filter(
                room_type_id=room_type_id,
                hold_expires_at__gt=now(),
                booking_start_date__lte=day,
                booking_end_date__gte=day,
            ).count()

            if bookings_count + active_booking_holds_count >= total_slots:
                return False

        return True

    # Others -----------------------------------------------------------------

    @staticmethod
    def authorize_get_hotel_of_room_type(request, pk):
        AppUserService.get_current_app_user(request)
        RoomTypeService.retrieve_room_type(pk)

    @staticmethod
    def get_hotel_of_room_type(pk):
        room_type = RoomTypeService.retrieve_room_type(pk)
        return room_type.hotel
