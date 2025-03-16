from django.utils.timezone import now, timedelta
from pawtel.booking_holds.models import BookingHold
from pawtel.booking_holds.serializers import BookingHoldSerializer
from pawtel.customers.services import CustomerService
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class BookingHoldService:

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_booking_hold(pk):
        try:
            return BookingHold.objects.get(pk=pk)
        except BookingHold.DoesNotExist:
            raise NotFound(detail=f"BookingHold not found.")

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def authorize_delete_booking_hold(request, pk):
        customer = CustomerService.get_current_customer(request)
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)

        if not booking_hold:
            raise NotFound("BookingHold does not exist.")

        if (not customer.user.is_active) or (booking_hold.customer.id != customer.id):
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def delete_booking_hold(pk):
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)
        booking_hold.delete()

    # POST -------------------------------------------------------------------

    @staticmethod
    def authorize_booking_hold_create(request):
        customer = CustomerService.get_current_customer(request)

        if not customer.user.is_active:
            raise PermissionDenied("Permission denied.")

        if BookingHoldService.has_customer_booking_hold(customer.id):
            raise PermissionDenied("Customer already has booking hold.")

    @staticmethod
    def serialize_input_booking_hold_create(request):
        context = {"request": request}

        current_customer_id = CustomerService.get_current_customer(request).id
        hold_expires_at = now() + timedelta(minutes=10)

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

        if (not room_type) or (room_type.is_archived):
            raise NotFound("RoomType does not exist.")

        # check there is vacancy

    @staticmethod
    def create_booking_hold(input_serializer):
        booking_hold = input_serializer.save()
        return booking_hold

    @staticmethod
    def serialize_output_booking_hold(booking_hold):
        return BookingHoldSerializer(booking_hold).data

    # Others -----------------------------------------------------------------

    @staticmethod
    def has_customer_booking_hold(customer_id):
        return BookingHold.objects.filter(customer_id=customer_id).exists()

    @staticmethod
    def count_active_booking_holds_of_room_type(room_type_id):
        return BookingHold.objects.filter(
            room_type_id=room_type_id, hold_expires_at__gt=now()
        ).count()
