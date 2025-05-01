from django.utils.timezone import now, timedelta
from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.booking_holds.models import BookingHold
from pawtel.booking_holds.serializers import BookingHoldSerializer
from pawtel.customers.services import CustomerService
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.permission_services import PermissionService
from pawtel.room_types.services import RoomTypeService
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class BookingHoldService:

    # Expiration -------------------------------------------------------------

    __HOLD_EXPIRATION_DURATION = timedelta(minutes=10)

    @staticmethod
    def __calculate_hold_expiry():
        return now() + BookingHoldService.__HOLD_EXPIRATION_DURATION

    # Authorization ----------------------------------------------------------

    @staticmethod
    def authorize_action_booking_hold(
        request, action_name, booking_hold_id=None, check_ownership=False
    ):
        role_user = AppUserService.get_current_role_user(request)
        HotelOwnerService.check_approval_hotel_owner(role_user)
        PermissionService.check_permission_booking_hold_service(role_user, action_name)

        if booking_hold_id:
            booking_hold = BookingHoldService.retrieve_booking_hold(booking_hold_id)
            if check_ownership:
                BookingHoldService.__check_ownership_booking_hold_service(
                    role_user, booking_hold
                )

        return role_user

    @staticmethod
    def __check_ownership_booking_hold_service(role_user, booking_hold):
        if role_user.user.role == UserRole.ADMIN:
            return

        elif role_user.user.role == UserRole.CUSTOMER:
            if booking_hold.customer.id != role_user.id:
                raise PermissionDenied("Permiso denegado.")

        else:
            raise PermissionDenied("Permiso denegado.")

    # Serialization ----------------------------------------------------------

    @staticmethod
    def serialize_input_booking_hold_create(request):
        context = {"request": request}

        current_customer_id = CustomerService.get_current_customer(request).id
        hold_expires_at = BookingHoldService.__calculate_hold_expiry()

        data = request.data.copy()
        data["customer"] = current_customer_id
        data["hold_expires_at"] = hold_expires_at

        serializer = BookingHoldSerializer(data=data, context=context)
        return serializer

    @staticmethod
    def serialize_output_booking_hold(booking_hold, many=False):
        return BookingHoldSerializer(booking_hold, many=many).data

    # Validations ------------------------------------------------------------

    @staticmethod
    def validate_booking_hold_create(input_serializer, customer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        room_type = input_serializer.validated_data.get("room_type")
        booking_start_date = input_serializer.validated_data.get("booking_start_date")
        booking_end_date = input_serializer.validated_data.get("booking_end_date")

        if BookingHoldService.has_customer_active_booking_hold(customer.id):
            BookingHoldService.delete_booking_holds_of_customer(customer.id)

        is_room_type_available = RoomTypeService.is_room_type_available(
            room_type.id, booking_start_date, booking_end_date
        )
        if not is_room_type_available:
            raise ValidationError(
                {
                    "room_type": "El tipo de habitación no se encuentra disponible en esta fecha."
                }
            )

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_booking_hold(pk):
        try:
            return BookingHold.objects.get(pk=pk)
        except BookingHold.DoesNotExist:
            raise NotFound(detail="Booking hold no encontrado.")

    @staticmethod
    def list_booking_holds():
        return BookingHold.objects.all()

    @staticmethod
    def has_customer_active_booking_hold(customer_id):
        return BookingHold.objects.filter(
            customer_id=customer_id, hold_expires_at__gt=now()
        ).exists()

    @staticmethod
    def has_customer_active_booking_hold_of_room_type(customer_id, room_type_id):
        return BookingHold.objects.filter(
            customer_id=customer_id,
            room_type_id=room_type_id,
            hold_expires_at__gt=now(),
        ).exists()

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_booking_hold(pk):
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)
        booking_hold.delete()

    @staticmethod
    def delete_booking_holds_of_customer(customer_id):
        booking_holds_to_delete = BookingHold.objects.filter(customer_id=customer_id)
        if booking_holds_to_delete.exists():
            booking_holds_to_delete.delete()

    # POST -------------------------------------------------------------------

    @staticmethod
    def create_booking_hold(input_serializer):
        booking_hold = input_serializer.save()
        return booking_hold
