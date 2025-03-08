from django.shortcuts import get_object_or_404
from pawtel.room_types.models import RoomType
from rest_framework.exceptions import ValidationError

from .models import Room


class RoomService:
    @staticmethod
    def get_all_rooms():
        return Room.objects.filter(is_archived=False)

    @staticmethod
    def get_room_by_id(room_id):
        return Room.objects.filter(id=room_id, is_archived=False).first()

    @staticmethod
    def create_room(data):
        room_type = RoomType.objects.get(id=data["room_type_id"])
        return Room.objects.create(
            room_type=room_type,
            name=data["name"],
            is_archived=data.get("is_archived", False),
        )

    @staticmethod
    def update_room(room_id, data):
        room = get_object_or_404(Room, id=room_id)
        required_fields = ["room_type_id", "name", "is_archived"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError(
                f"The following required fields are missing: {', '.join(missing_fields)}"
            )
        room.room_type = RoomType.objects.get(id=data["room_type_id"])
        room.name = data["name"]
        room.is_archived = data["is_archived"]
        room.save()
        return room

    @staticmethod
    def partial_update_room(room_id, data):
        room = get_object_or_404(Room, id=room_id)
        if "room_type_id" in data:
            room.room_type = RoomType.objects.get(id=data["room_type_id"])
        if "name" in data:
            room.name = data["name"]
        if "is_archived" in data:
            room.is_archived = data["is_archived"]
        room.save()
        return room

    @staticmethod
    def destroy_room(room_id):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return None
