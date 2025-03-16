from pawtel.base_serializer import BaseSerializer
from pawtel.booking_hold.models import BookingHold


class BookingHoldSerializer(BaseSerializer):

    fields_required_for_post = []
    fields_editable = []
    fields_not_readable = []

    class Meta:
        model = BookingHold
        fields = ["id", "hold_expires_at", "customer", "room_type"]
        extra_kwargs = {
            "id": {"read_only": True},
            "hold_expires_at": {"read_only": True, "allow_null": False},
            "customer": {"read_only": True, "allow_null": False},
            "room_type": {"read_only": True, "allow_null": False},
        }
