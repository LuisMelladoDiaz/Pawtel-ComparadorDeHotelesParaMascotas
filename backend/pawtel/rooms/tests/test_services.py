from django.test import TestCase
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room
from pawtel.rooms.services import RoomService


class RoomServiceTests(TestCase):
    def setUp(self):

        self.owner = HotelOwner.objects.create(username="testuser")
        self.hotel = Hotel.objects.create(name="Hotel Pawtel", hotel_owner=self.owner)

        self.room_type = RoomType.objects.create(
            name="Suite",
            description="Luxury suite for pets",
            capacity=10,
            price_per_night=100.00,
            pet_type="DOG",
            hotel=self.hotel,
        )

        self.room1 = Room.objects.create(
            room_type=self.room_type, name="Room 1", is_archived=False
        )

        self.room2 = Room.objects.create(
            room_type=self.room_type, name="Room 2", is_archived=True
        )

    def test_get_all_rooms(self):
        rooms = RoomService.get_all_rooms()
        self.assertIn(self.room1, rooms)
        self.assertNotIn(self.room2, rooms)

    def test_get_room_by_id(self):
        room = RoomService.get_room_by_id(self.room1.id)
        self.assertEqual(room, self.room1)
        room_archived = RoomService.get_room_by_id(self.room2.id)
        self.assertIsNone(room_archived)

    def test_create_room(self):
        data = {"room_type_id": self.room_type.id, "name": "Room 3"}
        new_room = RoomService.create_room(data)
        self.assertEqual(new_room.name, "Room 3")
        self.assertFalse(new_room.is_archived)

    def test_update_room(self):
        data = {
            "room_type_id": self.room_type.id,
            "name": "Updated Room 1",
            "is_archived": True,
        }
        updated_room = RoomService.update_room(self.room1.id, data)
        self.assertEqual(updated_room.name, "Updated Room 1")
        self.assertTrue(updated_room.is_archived)

    def test_partial_update_room(self):
        data = {"name": "Partially Updated Room 1"}
        updated_room = RoomService.partial_update_room(self.room1.id, data)
        self.assertEqual(updated_room.name, "Partially Updated Room 1")
        self.assertFalse(updated_room.is_archived)

    def test_destroy_room(self):
        room_id = self.room1.id
        RoomService.destroy_room(room_id)
        self.assertIsNone(RoomService.get_room_by_id(room_id))
