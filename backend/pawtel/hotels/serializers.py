from rest_framework import serializers
from pawtel.hotels.models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            "id", "name", "address", "city", "description", "hotel_owner"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"required": True, "max_length": 100, "allow_null": False},
            "address": {"required": True, "max_length": 100, "allow_null": False},
            "city": {"required": True, "max_length": 50, "allow_null": False},
            "description": {"required": True, "max_length": 300, "allow_null": False},
            "hotel_owner": {"required": True, "allow_null": False},
        }
