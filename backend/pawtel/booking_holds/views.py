import inspect

from pawtel.booking_holds.models import BookingHold
from pawtel.booking_holds.serializers import BookingHoldSerializer
from pawtel.booking_holds.services import BookingHoldService
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class BookingHoldViewSet(viewsets.ModelViewSet):
    queryset = BookingHold.objects.all()
    serializer_class = BookingHoldSerializer

    # Default CRUD -----------------------------------------------------------

    def list(self, request):
        action_name = inspect.currentframe().f_code.co_name
        BookingHoldService.authorize_action_booking_hold(request, action_name)
        booking_holds = BookingHoldService.list_booking_holds()
        output_serializer_data = BookingHoldService.serialize_output_booking_hold(
            booking_holds, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        BookingHoldService.authorize_action_booking_hold(
            request, action_name, booking_hold_id=pk
        )
        booking_hold = BookingHoldService.retrieve_booking_hold(pk)
        output_serializer_data = BookingHoldService.serialize_output_booking_hold(
            booking_hold
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        action_name = inspect.currentframe().f_code.co_name
        customer = BookingHoldService.authorize_action_booking_hold(
            request, action_name
        )
        input_serializer = BookingHoldService.serialize_input_booking_hold_create(
            request
        )
        BookingHoldService.validate_booking_hold_create(input_serializer, customer)
        booking_hold_added = BookingHoldService.create_booking_hold(input_serializer)
        output_serializer_data = BookingHoldService.serialize_output_booking_hold(
            booking_hold_added
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")

    def partial_update(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")

    def destroy(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        BookingHoldService.authorize_action_booking_hold(
            request, action_name, booking_hold_id=pk
        )
        BookingHoldService.delete_booking_hold(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
