from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.permission_services import PermissionService
from rest_framework.exceptions import NotFound, PermissionDenied


class BookingService:

    # Authorization ----------------------------------------------------------

    def authorize_action_booking_level_1(request, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_booking_role_permission(role_user, action_name)
        return role_user

    def authorize_action_booking_level_2(request, booking_id, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_booking_role_permission(role_user, action_name)
        BookingService.retrieve_booking(booking_id)
        return role_user

    def authorize_action_booking_level_3(request, booking_id, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_booking_role_permission(role_user, action_name)
        booking = BookingService.retrieve_booking(booking_id)
        BookingService.check_ownership_booking_service(role_user, booking)
        return role_user

    def check_ownership_booking_service(role_user, booking):
        if role_user.user.role == UserRole.ADMIN:
            return

        elif role_user.user.role == UserRole.CUSTOMER:
            if booking.customer.id != role_user.id:
                raise PermissionDenied("Permission denied.")

        else:
            raise PermissionDenied("Permission denied.")

    # Serialization -----------------------------------------------------------------

    @staticmethod
    def serialize_output_booking(booking, many=False):
        return BookingSerializer(booking, many=many).data

    #  GET Methods --------------------------------------------------------

    @staticmethod
    def list_bookings():
        return Booking.objects.all()

    @staticmethod
    def retrieve_booking(pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound(detail="Booking not found.")

    @staticmethod
    def count_bookings_of_room_type_at_date(room_type_id, date_to_check):
        return Booking.objects.filter(
            room_type_id=room_type_id,
            start_date__lte=date_to_check,  # Booking started before or on this day
            end_date__gte=date_to_check,  # Booking ends after or on this day
        ).count()
