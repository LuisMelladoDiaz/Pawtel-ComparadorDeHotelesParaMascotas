from pawtel.hotels.models import Hotel
from rest_framework import serializers


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name", "address", "city", "description", "hotel_owner"]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_archived": {"read_only": True, "allow_null": False},
            "name": {"required": True, "max_length": 100, "allow_null": False},
            "address": {"required": True, "max_length": 100, "allow_null": False},
            "city": {"required": True, "max_length": 50, "allow_null": False},
            "description": {"required": True, "max_length": 300, "allow_null": False},
            "hotel_owner": {"required": True, "allow_null": False},
        }
