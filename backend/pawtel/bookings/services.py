import json
from datetime import datetime

import stripe
from django.conf import settings
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.services import CustomerService
from pawtel.permission_services import PermissionService
from pawtel.room_types.models import RoomType
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY
secret_endpoint = settings.STRIPE_SECRET_ENDPOINT


class BookingService:

    # Authorization ----------------------------------------------------------

    def authorize_action_booking(
        request, action_name, booking_id=None, check_ownership=False
    ):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_booking_service(role_user, action_name)

        if booking_id:
            booking = BookingService.retrieve_booking(booking_id)
            if check_ownership:
                BookingService.__check_ownership_booking_service(role_user, booking)

        return role_user

    def __check_ownership_booking_service(role_user, booking):
        if role_user.user.role == UserRole.ADMIN:
            return

        elif role_user.user.role == UserRole.CUSTOMER:
            if booking.customer.id != role_user.id:
                raise PermissionDenied("Permiso denegado.")

        elif role_user.user.role == UserRole.HOTEL_OWNER:
            if booking.room_type.hotel.hotel_owner.id != role_user.id:
                raise PermissionDenied("Permiso denegado.")

        else:
            raise PermissionDenied("Permiso denegado.")

    # Serialization -----------------------------------------------------------------

    @staticmethod
    def serialize_output_booking(booking, many=False):
        return BookingSerializer(booking, many=many).data

    # Authorization -----------------------------------------------------

    # TODO This auth with the news auth_action_levels
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
            raise NotFound(detail="Reserva no encontrada.")

    @staticmethod
    def count_bookings_of_room_type_at_date(room_type_id, date_to_check):
        return Booking.objects.filter(
            room_type_id=room_type_id,
            start_date__lte=date_to_check,  # Booking started before or on this day
            end_date__gte=date_to_check,  # Booking ends after or on this day
        ).count()

    #  POST Methods -------------------------------------------------------

    @staticmethod
    def serialize_input_booking_create(request):
        from pawtel.room_types.services import RoomTypeService

        # Hack to get the current customer id
        if hasattr(request, "user"):
            current_customer_id = CustomerService.get_current_customer(request).id
            data = request.data.copy()
            data["customer"] = current_customer_id
        else:
            data = request
        room_type_price = RoomTypeService.retrieve_room_type(
            data["room_type"]
        ).price_per_night
        total_price = (
            room_type_price
            * (
                datetime.strptime(data["end_date"], "%Y-%m-%d").date()
                - datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            ).days
        )
        data["total_price"] = total_price
        return BookingSerializer(data=data)

    @staticmethod
    def validate_create_booking(request, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        customer = CustomerService.get_current_customer(request)

        room_id = input_serializer.validated_data.get("room_type").id

        try:
            room_type = RoomType.objects.get(id=room_id)
        except RoomType.DoesNotExist:
            raise NotFound("El tipo de habitación no existe.")

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
                "Un cliente puede tener diferentes reservas de la misma habitación pero que no coincidan."
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
            Booking(**input_serializer.validated_data)
        )
        customer = CustomerService.retrieve_customer(output_serializer.get("customer"))
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
                success_url=str(settings.FRONTEND_URL + "/"),
                cancel_url=str(settings.FRONTEND_URL + "/hotels/"),
                customer_email=customer.user.email,
            )

            return JsonResponse({"url": session.url})
        except Exception:
            return Response(
                {"error": "Algo salió mal."},
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
            print(e)
            return HttpResponse(status=400)

        if event.type == "checkout.session.completed":

            booking_json = json.loads(
                event.data.object.metadata.get("booking")
            )  # metadata contains the booking JSON in plain text
            booking = BookingService.serialize_input_booking_create(booking_json)
            booking.is_valid()
            booking.save()
            # TODO remove the asociated booking_hold

        return HttpResponse(status=200)
