from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.services import CustomerService
from rest_framework.exceptions import NotFound, PermissionDenied


class BookingService:

    # Common ------------------------------------------------------------

    @staticmethod
    def serialize_output_booking(booking, many=False):
        return BookingSerializer(booking, many=many).data

    # Authorization -----------------------------------------------------

    @staticmethod
    def authorize_action_booking(request, pk):
        booking = BookingService.retrieve_booking(pk)
        customer = CustomerService.get_current_customer(request)
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
    

    @staticmethod
    def list_bookings_by_hotel(hotel_id):
        bookings = Booking.objects.filter(room_type__hotel__id=hotel_id)
        return bookings

    @staticmethod
    def list_bookings_by_customer(customer_id):
        bookings = Booking.objects.filter(customer_id=customer_id)
        return bookings