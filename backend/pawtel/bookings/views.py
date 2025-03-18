import inspect

from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.bookings.services import BookingService
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        # In the future it will be restricted to admin onlyl
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = BookingService.check_permission(
            request.user, action_name
        )
        bookings = BookingService.list_bookings(permission_granted, user_type)
        output_serializer_data = BookingService.serialize_output_booking(
            bookings, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = BookingService.check_permission(
            request.user, action_name
        )
        BookingService.authorize_action_booking(
            request, pk, permission_granted, user_type
        )
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
