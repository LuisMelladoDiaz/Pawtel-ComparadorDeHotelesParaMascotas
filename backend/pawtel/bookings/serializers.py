from decimal import Decimal

from pawtel.base_serializer import BaseSerializer
from pawtel.bookings.models import Booking
from rest_framework import serializers


class BookingSerializer(BaseSerializer):
    fields_required_for_post = [
        "start_date",
        "end_date",
        "total_price",
        "customer",
        "room_type",
    ]
    fields_editable = []
    fields_not_readable = []

    hotel_id = serializers.SerializerMethodField()

    def get_hotel_id(self, obj):
        return (
            obj.get("room_type").hotel.id
            if obj.get("room_type") and obj.get("room_type").hotel
            else None
        )

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
