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
        "use_paw_points",
        "discount",
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
            "use_paw_points",
            "discount",
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
                "allow_null": False,
                "min_value": Decimal("1.00"),
                "max_digits": 10,
                "decimal_places": 2,
            },
            "use_paw_points": {"allow_null": False},
            "discount": {
                "allow_null": False,
                "min_value": Decimal("0.00"),
                "max_digits": 10,
                "decimal_places": 2,
            },
            "customer": {"allow_null": False},
            "room_type": {"allow_null": False},
        }
