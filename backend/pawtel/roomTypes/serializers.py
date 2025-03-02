from pawtel.roomTypes.models import RoomType
from rest_framework import serializers


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            "id",
            "name",
            "description",
            "capacity",
            "price_per_night",
            "pet_type",
            "hotel",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_archived": {"read_only": True, "allow_null": False},
            "name": {"required": True, "max_length": 50, "allow_null": False},
            "description": {"required": True, "max_length": 300, "allow_null": False},
            "capacity": {"required": True, "min_value": 1, "allow_null": False},
            "price_per_night": {
                "required": True,
                "min_value": 1.00,
                "max_digits": 6,
                "decimal_places": 2,
                "allow_null": False,
            },
            "pet_type": {"required": True, "allow_null": False},
            "hotel": {"required": True, "allow_null": False},
        }
