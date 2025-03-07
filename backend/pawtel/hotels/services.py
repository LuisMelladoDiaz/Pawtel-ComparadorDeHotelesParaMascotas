from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from pawtel.room_types.serializers import RoomTypeSerializer
from pawtel.rooms.models import Room
from rest_framework.exceptions import NotFound, PermissionDenied


class HotelService:
    def get_all_room_types_of_hotel(hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            raise NotFound(f"Hotel with id {hotel_id} not found.")

        room_types = RoomType.objects.filter(hotel=hotel)
        return RoomTypeSerializer(room_types, many=True).data

    def get_total_vacancy_for_each_room_type_of_hotel(hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            raise NotFound(f"Hotel with id {hotel_id} not found.")

        room_types = RoomType.objects.filter(hotel=hotel)

        vacancy_data = []

        for room_type in room_types:
            rooms = Room.objects.filter(room_type=room_type).count()
            total_vacancy = room_type.capacity * rooms
            vacancy_data.append(
                {"room_type_id": room_type.id, "total_vacancy": total_vacancy}
            )

        return vacancy_data

    def check_if_archived(hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            if hotel.is_archived:
                raise PermissionDenied(
                    "El hotel está archivado. No se puede realizar esta operación."
                )
        except Hotel.DoesNotExist:
            raise NotFound(f"Hotel with id {hotel_id} not found.")
