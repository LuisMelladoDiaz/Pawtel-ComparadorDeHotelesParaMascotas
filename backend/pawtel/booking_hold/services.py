from django.utils.timezone import now, timedelta
from pawtel.booking_hold.models import BookingHold
from pawtel.booking_hold.serializers import BookingHoldSerializer
from pawtel.customers.services import CustomerService
from pawtel.room_types.services import RoomTypeService
from rest_framework.exceptions import NotFound, PermissionDenied


class BookingHoldService:

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_booking_hold(pk):
        try:
            return BookingHoldService.objects.get(pk=pk)
        except BookingHoldService.DoesNotExist:
            raise NotFound(detail=f"BookingHold not found.")

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def authorize_delete_booking_hold(request, pk):
        customer = CustomerService.get_current_customer(request)
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)

        if not booking_hold:
            raise NotFound("BookingHold does not exist.")

        if (not customer.is_active) or (booking_hold.customer.id != customer.id):
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def delete_booking_hold_of_room_type(pk):
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)
        booking_hold.delete()

    # POST -------------------------------------------------------------------

    @staticmethod
    def authorize_add_booking_hold_of_room_type(request, room_type_id):
        room_type = RoomTypeService.retrieve_room_type(room_type_id)
        customer = CustomerService.get_current_customer(request)

        if (not room_type) or (room_type.is_archived):
            raise NotFound("RoomType does not exist.")

        if not customer.is_active:
            raise PermissionDenied("Permission denied.")

        if BookingHoldService.has_customer_booking_hold():
            raise PermissionDenied("Customer already has booking hold.")

    @staticmethod
    def validate_add_booking_hold_of_room_type():
        # check there is vacancy
        pass

    @staticmethod
    def add_booking_hold_of_room_type(request, room_type_id):
        room_type_id = RoomTypeService.retrieve_room_type(room_type_id).id
        customer_id = CustomerService.get_current_customer(request).id
        booking_hold = BookingHold.objects.create(
            hold_expires_at=now() + timedelta(minutes=10),
            customer_id=customer_id,
            room_type_id=room_type_id,
        )
        return booking_hold

    @staticmethod
    def serialize_output_booking_hold(booking_hold):
        return BookingHoldSerializer(booking_hold).data

    # Others -----------------------------------------------------------------

    @staticmethod
    def has_customer_booking_hold(customer_id):
        return BookingHoldService.objects.filter(customer_id=customer_id).exists()

    @staticmethod
    def count_active_booking_holds_of_room_type(room_type_id):
        return BookingHold.objects.filter(
            room_type_id=room_type_id, hold_expires_at__gt=now()
        ).count()
