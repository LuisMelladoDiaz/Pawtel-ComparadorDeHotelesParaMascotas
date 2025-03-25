from django.views.decorators.csrf import csrf_exempt
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.bookings.services import BookingService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        ##! TODO: In the future it will be restricted to admin onlyl
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

    def create(self, request):
        BookingService.authorize_create_booking(request)
        input_serializer = BookingService.serialize_input_booking_create(request.data)
        BookingService.validate_create_booking(request, input_serializer)
        response = BookingService.create_booking(input_serializer)
        return response

    @csrf_exempt
    @action(detail=False, methods=["post"], url_path="stripe")
    def stripe_response(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        response = BookingService.stripe_response_manager(payload, sig_header)
        return response

    # Forbidden Methods ----------------------------------------------------

    def update(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")

    def partial_update(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")

    def destroy(self, request, pk=None):
        raise MethodNotAllowed("This operation is forbidden.")
