from pawtel.base_serializer import BaseSerializer
from pawtel.rooms.models import Room


class RoomSerializer(BaseSerializer):

    fields_required_for_post = ["name", "room_type"]
    fields_editable = ["name"]
    fields_not_readable = []

    class Meta:
        model = Room
        fields = ["id", "is_archived", "name", "room_type"]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_archived": {"read_only": True},
            "name": {"max_length": 50, "allow_null": False},
            "room_type": {"allow_null": False},
        }
