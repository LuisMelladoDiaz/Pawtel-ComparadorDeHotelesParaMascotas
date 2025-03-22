from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.bookings.services import BookingService
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ["get"]

    def list(self, request):
        # In the future it will be restricted to admin onlyl
        bookings = BookingService.list_bookings()
        output_serializer_data = BookingService.serialize_output_booking(
            bookings, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        BookingService.authorize_action_booking(request, pk)
        booking = BookingService.retrieve_booking(pk)
        output_serializer_data = BookingService.serialize_output_booking(booking)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    # Forbidden Methods ----------------------------------------------------

    def create(self, request):
        raise PermissionDenied("This operation is forbidden.")

    def update(self, request, pk=None):
        raise PermissionDenied("This operation is forbidden.")

    def partial_update(self, request, pk=None):
        raise PermissionDenied("This operation is forbidden.")

    def destroy(self, request, pk=None):
        raise PermissionDenied("This operation is forbidden.")
