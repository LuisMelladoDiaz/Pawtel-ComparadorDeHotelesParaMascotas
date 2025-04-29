from datetime import date
from decimal import Decimal

from pawtel.base_serializer import BaseSerializer
from pawtel.bookings.models import Booking
from rest_framework import serializers


class BookingSerializer(BaseSerializer):
    fields_required_for_post = [
        "start_date",
        "end_date",
        "total_price",  # derived
        "customer",
        "room_type",
    ]
    fields_editable = []
    fields_not_readable = []

    hotel_id = serializers.SerializerMethodField()

    def get_hotel_id(self, obj):
        return obj.room_type.hotel.id if obj.room_type and obj.room_type.hotel else None

    class Meta:
        model = Booking
        fields = [
            "id",
            "creation_date",
            "start_date",
            "end_date",
            "total_price",
            "customer",
            "room_type",
            "hotel_id",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "creation_date": {"read_only": True},
            "start_date": {"allow_null": False},
            "end_date": {"allow_null": False},
            "total_price": {
                "min_value": Decimal("1.00"),
                "max_digits": 10,
                "decimal_places": 2,
            },
            "customer": {"allow_null": False},
            "room_type": {"allow_null": False},
        }

    # Added here because they are syntactic validations
    def validate(self, data):
        creation_date = data.get("creation_date")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        today = date.today()
        errors = {}

        if not creation_date:
            creation_date = today

        if creation_date > today:
            errors.setdefault("creation_date", []).append(
                "La fecha de comienzo de la reserva debe ser futura."
            )

        if start_date and start_date <= today:
            errors.setdefault("start_date", []).append(
                "La fecha de comienzo de la reserva debe ser futura."
            )

        if end_date and end_date <= today:
            errors.setdefault("end_date", []).append(
                "La fecha de finalización de la reserva debe ser futura."
            )

        if start_date and end_date:
            if end_date < start_date:
                errors.setdefault("end_date", []).append(
                    "La fecha de finalización de la reserva no puede ser anterior a la fecha de comienzo de la reserva."
                )

            if (end_date - start_date).days >= 186:
                errors.setdefault("end_date", []).append(
                    "La duración de la reserva no puede exceder 6 meses (186 días)."
                )

        if errors:
            raise serializers.ValidationError(errors)

        return data
