from datetime import date, datetime, timedelta

from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.booking_holds.models import BookingHold
from pawtel.bookings.models import Booking
from pawtel.bookings.services import BookingService
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.permission_services import PermissionService
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class RoomTypeService:

    THREE_YEARS = timedelta(days=3 * 365)

    # Authorization ----------------------------------------------------------

    def authorize_action_room_type(
        request, action_name, room_type_id=None, check_ownership=False
    ):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_room_type_service(role_user, action_name)

        if room_type_id:
            room_type = RoomTypeService.__perform_retrieve_room_type(
                role_user, room_type_id
            )
            if check_ownership:
                RoomTypeService.__check_ownership_room_type(role_user, room_type)
        return role_user

    def __perform_retrieve_room_type(role_user, room_type_id):
        if role_user.user.role == UserRole.ADMIN:
            return RoomTypeService.retrieve_room_type(room_type_id, allow_archived=True)
        else:
            return RoomTypeService.retrieve_room_type(room_type_id)

    def __check_ownership_room_type(role_user, room_type):
        if role_user.user.role == UserRole.ADMIN:
            return
        elif role_user.user.role == UserRole.HOTEL_OWNER:
            if room_type.hotel.hotel_owner.id != role_user.id:
                raise PermissionDenied("Permiso denegado.")
        else:
            raise PermissionDenied("Permiso denegado.")

    def check_admin_permission(role_user):
        allow_admin = False
        if role_user.user.role == UserRole.ADMIN:
            allow_admin = True
        return allow_admin

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
            raise ValidationError({"hotel": "Hotel inválido."})

        if name and RoomType.objects.filter(hotel_id=hotel.id, name=name).exists():
            raise ValidationError(
                {"name": "Nombre ya en uso para un tipo de habitación."}
            )

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
            raise ValidationError(
                {"name": "Nombre ya en uso para un tipo de habitación."}
            )

    @staticmethod
    def validate_room_type_is_available(start_date, end_date):
        if not start_date or not end_date:
            raise ValidationError(
                {"detail": "Formato de fecha inválido. Utilice yyyy-mm-dd."}
            )

        if end_date < start_date:
            raise ValidationError(
                {"end_date": "La fecha final no puede ser anterior a la inicial."}
            )

        if (end_date - start_date).days >= 186:
            raise ValidationError(
                {"detail": "La reserva no puede durar más de 6 meses (186 días)."}
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
            raise NotFound(detail="Tipo de habitación no encontrado.")

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

    def validate_room_type_deletion(pk):
        today = date.today()
        past_limit = today - RoomTypeService.THREE_YEARS
        delete = True

        recent_bookings = Booking.objects.filter(
            room_type_id=pk, start_date__range=(past_limit, today)
        )
        future_bookings = Booking.objects.filter(room_type_id=pk, start_date__gte=today)

        if future_bookings.exists():
            raise ValidationError(
                {
                    "detail": "No se puede borrar el objeto porque existe una reserva asociada próximamente."
                }
            )

        if recent_bookings.exists():
            delete = False

        return delete

    def archive_room_type(pk):
        RoomType.objects.filter(pk=pk).update(is_archived=True)

    # Availability -----------------------------------------------------------

    @staticmethod
    def parse_availability_dates(request):
        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")

        if not start_date_str or not end_date_str:
            raise ValidationError(
                {"detail": "La fecha inicial y la fecha final son obligatorias."}
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
        "hotel": int,
        "pet_type": str,
        "max_price_per_night": float,
        "min_price_per_night": float,
        "sort_by": str,
        "limit": int,
        "start_date": lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        "end_date": lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        "is_available": lambda v: str(v).lower() in ("true", "1"),  # If true or 1, True
    }

    @staticmethod
    def __validate_filters(filters):
        """Ensures filters are valid and have correct types."""
        if filters is None:
            return {}

        invalid_filters = [f for f in filters if f not in RoomTypeService.VALID_FILTERS]
        if invalid_filters:
            raise ValidationError(f"Invalid filters: {invalid_filters}")

        validated = {}
        for key, expected_type in RoomTypeService.VALID_FILTERS.items():
            if key in filters:
                try:
                    validated[key] = expected_type(filters[key])
                except (ValueError, TypeError):
                    pass
        return validated

    @staticmethod
    def __apply_filters(room_types, filters):
        q = Q()

        if "hotel" in filters:
            q &= Q(hotel__id=filters["hotel"])

        if "pet_type" in filters:
            q &= Q(pet_type=filters["pet_type"])

        if "max_price_per_night" in filters:
            q &= Q(price_per_night__lte=filters["max_price_per_night"])

        if "min_price_per_night" in filters:
            q &= Q(price_per_night__gte=filters["min_price_per_night"])

        filtered_room_types = room_types.filter(q).distinct()

        if (
            ("is_available" in filters)
            and ("start_date" in filters)
            and ("end_date" in filters)
            and filters.get("is_available") is True
        ):
            start_date = filters.get("start_date")
            end_date = filters.get("end_date")
            RoomTypeService.validate_room_type_is_available(start_date, end_date)

            filtered_room_types = [
                room_type
                for room_type in filtered_room_types
                if RoomTypeService.is_room_type_available(
                    room_type.id, start_date, end_date
                )
            ]

        return filtered_room_types

    @staticmethod
    def list_filtered_room_types(filters=None, allow_archived=False):
        if allow_archived:
            room_types = RoomType.objects.all()
        else:
            room_types = RoomType.objects.filter(is_archived=False)

        filters = RoomTypeService.__validate_filters(filters)
        room_types = RoomTypeService.__apply_filters(room_types, filters)

        if "sort_by" in filters:
            sort_field = filters["sort_by"]
            valid_sort_fields = ["pet_type", "price_per_night"]
            assert (
                sort_field.lstrip("-") in valid_sort_fields
            ), f"Filtro por orden inválido: {sort_field}"
            room_types = room_types.order_by(sort_field)

        if "limit" in filters:
            room_types = room_types[: filters["limit"]]

        return room_types
