from django.forms import ValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, NotFound
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.services import CustomerService  
from pawtel.room_types.models import RoomType

class BookingService:

    # Common ------------------------------------------------------------

    @staticmethod
    def serialize_output_booking(booking, many=False):
        return BookingSerializer(booking, many=many).data

    # Authorization -----------------------------------------------------

    @staticmethod
    def authorize_action_booking(request, pk):
        booking = BookingService.retrieve_booking(pk)
        customer = CustomerService.get_current_customer(request)  # Obtener el cliente
        if not booking:
            raise NotFound("Booking does not exist.")

        if booking.customer.id != customer.id:
            raise PermissionDenied("Permission denied.")

    #  GET Methods --------------------------------------------------------

    @staticmethod
    def list_bookings():
        bookings = Booking.objects.all()
        return bookings


    @staticmethod
    def retrieve_booking(pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound(detail=f"Booking with id {pk} not found")


    

    # Create Method -----------------------------------------------------

    @staticmethod
    @transaction.atomic
    def create_booking(request, booking_data):
        customer = CustomerService.get_current_customer(request)  
        room_id = booking_data.get("room_type")
        try:
            room_type = RoomType.objects.get(id=room_id)
        except RoomType.DoesNotExist:
            raise NotFound("RoomType does not exist.")

        start_date = booking_data.get("start_date")
        end_date = booking_data.get("end_date")
        if end_date <= start_date:
            raise ValidationError({"end_date": "End date must be later than or equal to start date."})

        #Validate that the client does not have previous reservations for the same room in the same period
        overlapping_bookings = Booking.objects.filter(
            customer=customer,
            room_type=room_type,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if overlapping_bookings:
            raise ValidationError("A customer can have different bookings for the same room, but not overlapping.")

        price_per_night = room_type.price_per_night
        total_nights = (end_date - start_date).days
        total_price = round(price_per_night * total_nights, 2)  # 2 decimals

        #Create the booking
        booking = Booking.objects.create(
            customer=customer,
            room_type=room_type,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
        )

        return booking