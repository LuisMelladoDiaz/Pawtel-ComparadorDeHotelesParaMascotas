from pawtel.base_serializer import BaseSerializer
from pawtel.bookings.models import Booking


class BookingSerializer(BaseSerializer):
    fields_required_for_post = [
        "start_date",
        "end_date",
        "total_price",
        "customer",
        "room_type",
    ]
    fields_editable = ["start_date", "end_date", "total_price"]
    fields_not_readable = []

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
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "creation_date": {"read_only": True},
            "start_date": {"allow_null": False},
            "end_date": {"allow_null": False},
            "total_price": {
                "min_value": Decimal("1.00"),
                "decimal_places": 2,
                "allow_null": False,
            },
            "customer": {"allow_null": False},
            "room_type": {"allow_null": False},
        }
