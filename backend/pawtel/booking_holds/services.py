from django.utils.timezone import now, timedelta
from pawtel.booking_holds.models import BookingHold
from pawtel.booking_holds.serializers import BookingHoldSerializer
from pawtel.customers.services import CustomerService
from pawtel.room_types.services import RoomTypeService
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class BookingHoldService:

    # Others -----------------------------------------------------------------

    __HOLD_EXPIRATION_DURATION = timedelta(minutes=10)

    @staticmethod
    def __calculate_hold_expiry():
        return now() + BookingHoldService.__HOLD_EXPIRATION_DURATION

    @staticmethod
    def authorize_generic_action_booking_hold(request, pk):
        customer = CustomerService.get_current_customer(request)
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)

        if booking_hold.customer.id != customer.id:
            raise PermissionDenied("Permission denied.")

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_booking_hold(pk):
        try:
            return BookingHold.objects.get(pk=pk)
        except BookingHold.DoesNotExist:
            raise NotFound(detail="BookingHold not found.")

    @staticmethod
    def list_booking_holds():
        return BookingHold.objects.all()

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_booking_hold(pk):
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)
        booking_hold.delete()

    # POST -------------------------------------------------------------------

    @staticmethod
    def authorize_booking_hold_create(request):
        customer = CustomerService.get_current_customer(request)

        if BookingHoldService.has_customer_active_booking_hold(customer.id):
            raise PermissionDenied("Customer already has booking hold.")

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
    def validate_booking_hold_create(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        room_type = input_serializer.validated_data.get("room_type")
        booking_start_date = input_serializer.validated_data.get("booking_start_date")
        booking_end_date = input_serializer.validated_data.get("booking_end_date")

        if (not room_type) or (room_type.is_archived):
            raise NotFound("RoomType does not exist.")

        is_room_type_available = RoomTypeService.is_room_type_available(
            room_type.id, booking_start_date, booking_end_date
        )
        if not is_room_type_available:
            raise ValidationError(
                {"room_type": "RoomType is not available during indicated period."}
            )

    @staticmethod
    def create_booking_hold(input_serializer):
        booking_hold = input_serializer.save()
        return booking_hold

    @staticmethod
    def serialize_output_booking_hold(booking_hold, many=False):
        return BookingHoldSerializer(booking_hold, many=many).data

    # Others -----------------------------------------------------------------

    @staticmethod
    def has_customer_active_booking_hold(customer_id):
        return BookingHold.objects.filter(
            customer_id=customer_id, hold_expires_at__gt=now()
        ).exists()
