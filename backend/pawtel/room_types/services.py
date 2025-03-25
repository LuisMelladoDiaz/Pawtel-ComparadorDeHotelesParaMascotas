from datetime import datetime, timedelta

from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.booking_holds.models import BookingHold
from pawtel.bookings.services import BookingService
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.permission_services import PermissionService
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class RoomTypeService:

    # Authorization ----------------------------------------------------------

    def authorize_action_room_type_level_1(request, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_room_type_service(role_user, action_name)
        return role_user

    def authorize_action_room_type_level_2(request, room_type_id, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_room_type_service(role_user, action_name)
        RoomTypeService.retrieve_room_type(room_type_id)
        return role_user

    def authorize_action_room_type_level_3(request, room_type_id, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_room_type_service(role_user, action_name)
        room_type = RoomTypeService.retrieve_room_type(room_type_id)
        RoomTypeService.check_ownership_room_type(role_user, room_type)
        return role_user

    def check_ownership_room_type(role_user, room_type):
        if role_user.user.role == UserRole.ADMIN:
            return

        elif role_user.user.role == UserRole.HOTEL_OWNER:
            if room_type.hotel.hotel_owner.id != role_user.id:
                raise PermissionDenied("Permission denied.")

        else:
            raise PermissionDenied("Permission denied.")

    # Serialization -----------------------------------------------------------------

    @staticmethod
    def serialize_input_room_type_create(request):
        context = {"request": request}
        serializer = RoomTypeSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def serialize_input_room_type_update(request, pk):
        room_type = RoomTypeService.retrieve_room_type(pk)
        context = {"request": request}
        serializer = RoomTypeSerializer(
            instance=room_type, data=request.data, context=context
        )
        return serializer

    @staticmethod
    def serialize_output_room_type(room_type, many=False):
        return RoomTypeSerializer(room_type, many=many).data

    # Validations ------------------------------------------------------------

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
    def validate_room_type_available(start_date, end_date):
        if not start_date or not end_date:
            raise ValidationError({"detail": "Invalid date format. Use yyyy-mm-dd."})

        if end_date < start_date:
            raise ValidationError(
                {"end_date": "End date cannot be earlier than start date."}
            )

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

    @staticmethod
    def get_hotel_of_room_type(pk):
        room_type = RoomTypeService.retrieve_room_type(pk)
        return room_type.hotel

    # POST -------------------------------------------------------------------

    @staticmethod
    def create_room_type(input_serializer):
        room_type_created = input_serializer.save()
        return room_type_created

    # PUT/PATCH --------------------------------------------------------------

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

    # Filter -----------------------------------------------------------------

    VALID_FILTERS = {
        "pet_type": str,
        "max_price_per_night": float,
        "min_price_per_night": float,
        "sort_by": str,
        "limit": int,
        "start_date": lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        "end_date": lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
    }

    @staticmethod
    def validate_filters(filters):
        if filters is None:
            return {}
        assert all(
            f in RoomTypeService.VALID_FILTERS for f in filters
        ), f"Filtro inválido: {filters}"
        validated = {}
        for key, expected_type in RoomTypeService.VALID_FILTERS.items():
            if key in filters:
                try:
                    validated[key] = expected_type(filters[key])
                except (ValueError, TypeError):
                    pass
        return validated

    @staticmethod
    def apply_filters(room_types, filters):
        q = Q()

        if "pet_type" in filters:
            q &= Q(pet_type=filters["pet_type"])

        if "max_price_per_night" in filters:
            q &= Q(price_per_night__lte=filters["max_price_per_night"])

        if "min_price_per_night" in filters:
            q &= Q(price_per_night__gte=filters["min_price_per_night"])

        return room_types.filter(q).distinct()

    @staticmethod
    def list_filtered_room_types(hotel_id, filters=None):
        room_types = RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)

        filters = RoomTypeService.validate_filters(filters)
        room_types = RoomTypeService.apply_filters(room_types, filters)

        if "sort_by" in filters:
            sort_field = filters["sort_by"]
            valid_sort_fields = ["pet_type", "price_per_night"]
            assert (
                sort_field.lstrip("-") in valid_sort_fields
            ), f"Campo de ordenamiento inválido: {sort_field}"
            room_types = room_types.order_by(sort_field)

        if "limit" in filters:
            room_types = room_types[: filters["limit"]]

        return room_types
