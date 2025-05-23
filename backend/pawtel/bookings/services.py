import json
from datetime import datetime
from decimal import ROUND_HALF_DOWN, ROUND_HALF_UP, Decimal

import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.booking_holds.services import BookingHoldService
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.services import CustomerService
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.permission_services import PermissionService
from pawtel.room_types.services import RoomTypeService
from rest_framework import status
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY
secret_endpoint = settings.STRIPE_SECRET_ENDPOINT


class BookingService:

    DISCOUNT_PER_PAW_POINT = Decimal("0.05")
    PAW_POINTS_PER_EURO_SPENT = Decimal("1.00")

    # Authorization ----------------------------------------------------------

    @staticmethod
    def authorize_action_booking(
        request, action_name, booking_id=None, check_ownership=False
    ):
        role_user = AppUserService.get_current_role_user(request)
        HotelOwnerService.check_approval_hotel_owner(role_user)
        PermissionService.check_permission_booking_service(role_user, action_name)

        if booking_id:
            booking = BookingService.retrieve_booking(booking_id)
            if check_ownership:
                BookingService.__check_ownership_booking_service(role_user, booking)

        return role_user

    @staticmethod
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

    # Serialization ----------------------------------------------------------

    @staticmethod
    def serialize_output_booking(booking, many=False):
        return BookingSerializer(booking, many=many).data

    @staticmethod
    def serialize_input_booking_create(request):
        context = {"request": request}
        data = request.data.copy()

        current_customer = CustomerService.get_current_customer(request)
        data["customer"] = current_customer.id

        room_type = request.data.get("room_type")
        end_date = request.data.get("end_date")
        start_date = request.data.get("start_date")

        if room_type and end_date and start_date:
            room_type_price = RoomTypeService.retrieve_room_type(
                room_type
            ).price_per_night
            num_days_booking = (
                datetime.strptime(end_date, "%Y-%m-%d").date()
                - datetime.strptime(start_date, "%Y-%m-%d").date()
            ).days
            total_price = room_type_price * num_days_booking
            data["total_price"] = total_price
        else:
            pass  # Let the validate method raise the error

        discount = 0.00
        if data.get("use_paw_points") is True:
            all_paw_points = Decimal(current_customer.paw_points)
            max_discount = all_paw_points * BookingService.DISCOUNT_PER_PAW_POINT
            max_discount = max_discount.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )  # 2 decimals only
            discount = min(max_discount, total_price)
        data["discount"] = discount

        serializer = BookingSerializer(data=data, context=context)
        return serializer

    # Validations ------------------------------------------------------------

    @staticmethod
    def validate_create_booking(request, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        customer = CustomerService.get_current_customer(request)
        room_type_id = input_serializer.validated_data.get("room_type").id
        room_type = RoomTypeService.retrieve_room_type(room_type_id)
        start_date = input_serializer.validated_data.get("start_date")
        end_date = input_serializer.validated_data.get("end_date")

        # Validate that the client does not already have bookings for the same room in the same period
        overlapping_bookings = Booking.objects.filter(
            customer=customer,
            room_type=room_type,
            start_date__lt=end_date,
            end_date__gt=start_date,
        ).exists()

        if overlapping_bookings:
            raise ValidationError(
                "Un cliente puede tener diferentes reservas de la misma habitación pero no pueden coincidir en fecha."
            )

    # GET Methods ------------------------------------------------------------

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

    #  POST Methods ----------------------------------------------------------

    @staticmethod
    def create_booking(input_serializer):
        BookingHoldService.create_booking_hold_from_booking(input_serializer)
        stripe_api_response = BookingService.stripe_checkout_transference(
            input_serializer
        )
        return stripe_api_response

    @staticmethod
    def stripe_checkout_transference(input_serializer):
        """This calls Stripe API and obtains a Stripe payment session with the data of the booking."""

        total_price = input_serializer.validated_data.get("total_price")
        total_price = int(total_price * 100)
        discount = input_serializer.validated_data.get("discount")
        discount = int(discount * 100)

        room_type_name = input_serializer.validated_data.get("room_type").name
        room_type_description = input_serializer.validated_data.get(
            "room_type"
        ).description

        # Booking JSON must be saved in plain text
        output_serializer = BookingService.serialize_output_booking(
            Booking(**input_serializer.validated_data)
        )
        customer = CustomerService.retrieve_customer(output_serializer.get("customer"))
        booking_json_str = json.dumps(output_serializer)

        response = None

        try:
            line_items = [
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": room_type_name,
                            "description": room_type_description,
                        },
                        "unit_amount": total_price - discount,
                    },
                    "quantity": 1,
                },
            ]

            session = stripe.checkout.Session.create(
                line_items=line_items,
                metadata={"booking": booking_json_str},
                mode="payment",
                success_url=str(settings.FRONTEND_URL + "/"),
                cancel_url=str(settings.FRONTEND_URL + "/hotels/"),
                customer_email=customer.user.email,
            )

            response = JsonResponse({"url": session.url})

        except Exception:
            response = Response(
                {"error": "Algo salió mal."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response

    @staticmethod
    @transaction.atomic
    def stripe_response_manager(payload, sig_header):
        event = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, secret_endpoint)
        except ValueError:  # as e:
            # Invalid payload
            # print(e)
            return HttpResponse(status=400)

        if event.type == "checkout.session.completed":

            booking_json = json.loads(
                event.data.object.metadata.get("booking")
            )  # metadata contains the booking JSON in plain text
            booking_serializer = BookingSerializer(data=booking_json)

            if booking_serializer.is_valid():
                booking = booking_serializer.save()
            else:
                return HttpResponse(status=400)

            BookingHoldService.delete_booking_holds_of_customer(booking.customer)

            BookingService.__recalculate_paw_points(booking_serializer)

        return HttpResponse(status=200)

    @staticmethod
    def __recalculate_paw_points(booking_serializer):
        if not booking_serializer.is_valid():
            return HttpResponse(status=400)

        customer = booking_serializer.validated_data.get("customer")
        total_price = Decimal(booking_serializer.validated_data.get("total_price"))
        discount = Decimal(booking_serializer.validated_data.get("discount"))
        paw_points_increment = 0

        paw_points_spent = discount / BookingService.DISCOUNT_PER_PAW_POINT
        paw_points_spent = paw_points_spent.quantize(
            Decimal("1."), rounding=ROUND_HALF_DOWN
        )  # no decimals
        paw_points_increment = -paw_points_spent

        new_price = total_price - discount
        paw_points_earned = new_price * BookingService.PAW_POINTS_PER_EURO_SPENT
        paw_points_earned = paw_points_earned.quantize(
            Decimal("1."), rounding=ROUND_HALF_UP
        )  # no decimals
        paw_points_increment += paw_points_earned

        CustomerService.add_paw_points(customer, paw_points_increment)
