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
        if data.get("hold_expires_at") and data["hold_expires_at"] < now():
            raise serializers.ValidationError(
                {"hold_expires_at": "Hold expiration date cannot be in the past."}
            )

        if data.get("booking_start_date") <= date.today():
            raise serializers.ValidationError(
                {"booking_start_date": "Booking start date must be in the future."}
            )

        if data.get("booking_end_date") <= date.today():
            raise serializers.ValidationError(
                {"booking_end_date": "Booking end date must be in the future."}
            )

        if data.get("booking_end_date") < data.get("booking_start_date"):
            raise serializers.ValidationError(
                {
                    "end_date": "Booking end date cannot be earlier than booking start date."
                }
            )

        return data
