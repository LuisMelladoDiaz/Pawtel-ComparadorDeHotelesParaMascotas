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
                "La fecha de expiración de la Booking Hold no puede ser pasada."
            )

        if booking_start_date <= date.today():
            errors.setdefault("booking_start_date", []).append(
                "La fecha de comienzo de la reserva debe ser futura."
            )

        if booking_end_date <= date.today():
            errors.setdefault("booking_end_date", []).append(
                "La fecha de finalización de la reserva debe ser futura."
            )

        if booking_end_date < booking_start_date:
            errors.setdefault("booking_end_date", []).append(
                "La fecha de finalización de la reserva no puede ser anterior a la fecha de comienzo de la reserva."
            )

        if (booking_end_date - booking_start_date).days >= 186:
            errors.setdefault("booking_end_date", []).append(
                "La duración de la reserva no puede exceder 6 meses (186 días)."
            )

        if errors:
            raise serializers.ValidationError(errors)

        return data
