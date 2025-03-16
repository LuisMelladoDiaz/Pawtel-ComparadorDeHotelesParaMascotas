from pawtel.booking_hold.models import BookingHold
from pawtel.booking_hold.serializers import BookingHoldSerializer
from pawtel.booking_hold.services import BookingHoldService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class BookingHoldViewSet(viewsets.ModelViewSet):
    queryset = BookingHold.objects.all()
    serializer_class = BookingHoldSerializer

    # Default CRUD -----------------------------------------------------------

    def list(self, request):
        raise PermissionDenied("This operation is forbidden.")

    def retrieve(self, request, pk=None):
        raise PermissionDenied("This operation is forbidden.")

    def create(self, request):
        raise PermissionDenied("This operation is forbidden.")

    def update(self, request, pk=None):
        raise PermissionDenied("This operation is forbidden.")

    def partial_update(self, request, pk=None):
        raise PermissionDenied("This operation is forbidden.")

    def destroy(self, request, pk=None):
        BookingHoldService.authorize_delete_booking_hold(request, pk)
        BookingHoldService.delete_booking_hold(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Others -----------------------------------------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="add_hold",
        url_name="add_hold_of_room_type",
    )
    def add_hold_of_room_type_during_booking_operation(self, request, pk=None):
        BookingHoldService.authorize_add_booking_hold_of_room_type(request, pk)
        BookingHoldService.validate_add_booking_hold_of_room_type(request)
        booking_hold_added = BookingHoldService.add_booking_hold_of_room_type()
        output_serializer_data = BookingHoldService.serialize_output_booking_hold(
            booking_hold_added
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)
