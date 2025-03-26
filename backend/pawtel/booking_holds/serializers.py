from datetime import date

from django.utils.timezone import now
from pawtel.base_serializer import BaseSerializer
from pawtel.booking_holds.models import BookingHold
from rest_framework import serializers


class BookingHoldSerializer(BaseSerializer):

    fields_required_for_post = [
        "hold_expires_at",
        "booking_start_date",
        "booking_end_date",
        "customer",
        "room_type",
    ]
    fields_editable = []
    fields_not_readable = []

    class Meta:
        model = BookingHold
        fields = [
            "id",
            "hold_expires_at",
            "booking_start_date",
            "booking_end_date",
            "customer",
            "room_type",
            "is_expired",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "hold_expires_at": {"allow_null": False},
            "booking_start_date": {"allow_null": False},
            "booking_end_date": {"allow_null": False},
            "customer": {"allow_null": False},
            "room_type": {"allow_null": False},
        }

    # Added here because they are syntactic validations
    def validate(self, data):
        hold_expires_at = data.get("hold_expires_at")
        booking_start_date = data.get("booking_start_date")
        booking_end_date = data.get("booking_end_date")

        errors = {}

        if hold_expires_at and hold_expires_at < now():
            errors.setdefault("hold_expires_at", []).append(
                "Hold expiration date cannot be in the past."
            )

        if booking_start_date <= date.today():
            errors.setdefault("booking_start_date", []).append(
                "Booking start date must be in the future."
            )

        if booking_end_date <= date.today():
            errors.setdefault("booking_end_date", []).append(
                "Booking end date must be in the future."
            )

        if booking_end_date < booking_start_date:
            errors.setdefault("booking_end_date", []).append(
                "Booking end date cannot be earlier than booking start date."
            )

        if (booking_end_date - booking_start_date).days >= 186:
            errors.setdefault("booking_end_date", []).append(
                "The booking duration cannot exceed 6 months (186 days)."
            )

        if errors:
            raise serializers.ValidationError(errors)

        return data
