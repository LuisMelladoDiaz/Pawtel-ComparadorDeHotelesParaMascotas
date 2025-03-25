import json
import os

import stripe
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
from pawtel.app_users.services import AppUserService
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.services import CustomerService
from pawtel.room_types.models import RoomType
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

load_dotenv()
stripe.api_key = str(os.getenv("STRIPE_SECRET_KEY"))
secret_endpoint = str(os.getenv("STRIPE_SECRET_ENDPOINT"))


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

        if booking.customer.id != customer.id:
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def authorize_create_booking(request):
        return AppUserService._AppUserService__authorize_action_app_user(
            request, request.user.id
        )

    #  GET Methods --------------------------------------------------------

    @staticmethod
    def list_bookings():
        return Booking.objects.all()

    @staticmethod
    def retrieve_booking(pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound(detail="Booking not found.")

    @staticmethod
    def count_bookings_of_room_type_at_date(room_type_id, date_to_check):
        return Booking.objects.filter(
            room_type_id=room_type_id,
            start_date__lte=date_to_check,  # Booking started before or on this day
            end_date__gte=date_to_check,  # Booking ends after or on this day
        ).count()

    #  POST Methods -------------------------------------------------------

    @staticmethod
    def serialize_input_booking_create(request_data):
        return BookingSerializer(data=request_data)

    @staticmethod
    def validate_create_booking(request, input_serializer):

        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        customer = CustomerService.get_current_customer(request)

        # TODO uncomment this validation
        # Auth validation
        # if not ( customer == input_serializer.validated_data.get("customer")):
        # raise ValidationError({"customer": "The customer in the request does not match the customer associated with the booking"})

        room_id = input_serializer.validated_data.get("room_type").id

        try:
            room_type = RoomType.objects.get(id=room_id)
        except RoomType.DoesNotExist:
            raise NotFound("RoomType does not exist.")

        start_date = input_serializer.validated_data.get("start_date")
        end_date = input_serializer.validated_data.get("end_date")

        # Validate that the client does not have previous reservations for the same room in the same period
        overlapping_bookings = Booking.objects.filter(
            customer=customer,
            room_type=room_type,
            start_date__lt=end_date,
            end_date__gt=start_date,
        ).exists()

        if overlapping_bookings:
            raise ValidationError(
                "A customer can have different bookings for the same room, but not overlapping."
            )

        # TODO: Implement validation for booking_holds

    @staticmethod
    def create_booking(input_serializer):
        # Stripe API Call
        response = BookingService.stripe_checkout_transference(input_serializer)
        # response = BookingService.stripe_response_manager(transference)
        return response

    @staticmethod
    def stripe_checkout_transference(input_serializer):
        total_price = input_serializer.validated_data.get("total_price")
        total_price = int(total_price * 100)
        room_type_name = input_serializer.validated_data.get("room_type").name
        room_type_description = input_serializer.validated_data.get(
            "room_type"
        ).description
        # Must save Booking JSON in plain text
        output_serializer = BookingService.serialize_output_booking(
            input_serializer.validated_data
        )
        booking_json_str = json.dumps(output_serializer)
        try:
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "product_data": {
                                "name": room_type_name,
                                "description": room_type_description,
                            },
                            "unit_amount": total_price,
                        },
                        "quantity": 1,
                    },
                ],
                metadata={"booking": booking_json_str},
                mode="payment",
                success_url=str(os.getenv("FRONTEND_URL") + "/"),
                cancel_url=str(os.getenv("FRONTEND_URL") + "/hotels/"),
            )

            return JsonResponse({"url": session.url})
        except:
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    @transaction.atomic
    def stripe_response_manager(payload, sig_header):

        event = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, secret_endpoint)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)

        if event.type == "checkout.session.completed":
            print(event.data.object.metadata)
            booking_json = json.loads(
                event.data.object.metadata.get("booking")
            )  # metadata contains the booking JSON in plain text
            booking = BookingService.serialize_input_booking_create(booking_json)
            booking.is_valid()
            booking.save()
            # TODO remove the asociated booking_hold

        return HttpResponse(status=200)
