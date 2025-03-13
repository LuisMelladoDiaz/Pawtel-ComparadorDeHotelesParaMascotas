from pawtel.base_serializer import BaseSerializer
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from django.db.models import Min, Max
from rest_framework import serializers

class HotelSerializer(BaseSerializer):
    fields_required_for_post = ["name", "address", "city", "description", "hotel_owner"]
    fields_editable = ["name", "address", "city", "description"]
    fields_not_readable = []

    cheapest_price = serializers.SerializerMethodField()
    most_expensive_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            "id",
            "is_archived",
            "name",
            "address",
            "city",
            "description",
            "hotel_owner",
            "cheapest_price",
            "most_expensive_price",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_archived": {"read_only": True},
            "name": {"max_length": 100, "allow_null": False},
            "address": {"max_length": 100, "allow_null": False},
            "city": {"max_length": 50, "allow_null": False},
            "description": {"max_length": 400, "allow_null": False},
            "hotel_owner": {"allow_null": False},
        }

    def get_cheapest_price(self, obj):
        cheapest = RoomType.objects.filter(hotel=obj).aggregate(min_price=Min("price_per_night"))["min_price"]
        return cheapest if cheapest is not None else None
    
    def get_most_expensive_price(self, obj):
        most_expensive = RoomType.objects.filter(hotel=obj).aggregate(max_price=Max("price_per_night"))["max_price"]
        return most_expensive if most_expensive is not None else None
