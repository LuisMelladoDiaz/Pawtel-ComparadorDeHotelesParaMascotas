from pawtel.base_serializer import BaseSerializer
from pawtel.hotels.models import Hotel


class HotelSerializer(BaseSerializer):

    fields_required_for_post = ["name", "address", "city", "description", "hotel_owner"]
    fields_editable = ["name", "address", "city", "description"]
    fields_not_readable = []

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
