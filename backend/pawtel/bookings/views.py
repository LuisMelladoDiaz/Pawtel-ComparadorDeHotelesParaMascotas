import inspect

from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.bookings.services import BookingService
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        action_name = inspect.currentframe().f_code.co_name
        BookingService.authorize_action_booking_level_1(request, action_name)
        bookings = BookingService.list_bookings()
        output_serializer_data = BookingService.serialize_output_booking(
            bookings, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        BookingService.authorize_action_booking_level_3(request, pk, action_name)
        booking = BookingService.retrieve_booking(pk)
        output_serializer_data = BookingService.serialize_output_booking(booking)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    # Forbidden Methods ----------------------------------------------------

    def create(self, request):
        raise MethodNotAllowed("This operation is forbidden.")

    def update(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")

    def partial_update(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")

    def destroy(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")
