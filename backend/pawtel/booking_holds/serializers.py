from pawtel.base_serializer import BaseSerializer
from pawtel.booking_holds.models import BookingHold


class BookingHoldSerializer(BaseSerializer):

    fields_required_for_post = ["hold_expires_at", "customer", "room_type"]
    fields_editable = []
    fields_not_readable = []

    class Meta:
        model = BookingHold
        fields = ["id", "hold_expires_at", "customer", "room_type", "is_expired"]
        extra_kwargs = {
            "id": {"read_only": True},
            "hold_expires_at": {"allow_null": False},
            "customer": {"allow_null": False},
            "room_type": {"allow_null": False},
        }
