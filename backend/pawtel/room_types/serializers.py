from decimal import Decimal

from pawtel.base_serializer import BaseSerializer
from pawtel.room_types.models import RoomType


class RoomTypeSerializer(BaseSerializer):

    fields_required_for_post = [
        "name",
        "description",
        "capacity",
        "num_rooms",
        "price_per_night",
        "pet_type",
        "hotel",
    ]
    fields_editable = [
        "name",
        "description",
        "capacity",
        "num_rooms",
        "price_per_night",
        "pet_type",
    ]
    fields_not_readable = []

    class Meta:
        model = RoomType
        fields = [
            "id",
            "is_archived",
            "name",
            "description",
            "capacity",
            "num_rooms",
            "price_per_night",
            "pet_type",
            "hotel",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_archived": {"read_only": True},
            "name": {"max_length": 50, "allow_null": False},
            "description": {"max_length": 300, "allow_null": False},
            "capacity": {"min_value": 1, "max_value": 200, "allow_null": False},
            "num_rooms": {"min_value": 0, "max_value": 200, "allow_null": False},
            "price_per_night": {
                "required": True,
                "min_value": Decimal("1.00"),
                "max_digits": 6,
                "decimal_places": 2,
                "allow_null": False,
            },
            "pet_type": {"allow_null": False},
            "hotel": {"allow_null": False},
        }
