from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from pawtel.room_types.services import RoomTypeService
from pawtel.rooms.models import Room


class RoomTypeServiceTests(TestCase):
    def setUp(self):
        self.app_user = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.owner = HotelOwner.objects.create(user_id=self.app_user.id)
        self.hotel = Hotel.objects.create(name="Hotel Pawtel", hotel_owner=self.owner)

        self.room_type_1 = RoomType.objects.create(
            name="Suite",
            description="Luxury suite for pets",
            capacity=10,
            price_per_night=100.00,
            pet_type="DOG",
            hotel=self.hotel,
            is_archived=False,
        )
        self.room_type_2 = RoomType.objects.create(
            name="Standard",
            description="Standard room for pets",
            capacity=5,
            price_per_night=50.00,
            pet_type="CAT",
            hotel=self.hotel,
            is_archived=True,
        )

        self.room1 = Room.objects.create(
            room_type=self.room_type_1, name="Room 1", is_archived=False
        )
        self.room2 = Room.objects.create(
            room_type=self.room_type_1, name="Room 2", is_archived=True
        )
        self.room3 = Room.objects.create(
            room_type=self.room_type_1, name="Room 3", is_archived=False
        )
        self.room4 = Room.objects.create(
            room_type=self.room_type_2, name="Room 4", is_archived=True
        )

    def test_get_total_vacancy_of_room_type_valid(self):
        total_vacancy = RoomTypeService.get_total_vacancy_of_room_type(
            room_type_id=self.room_type_1.id
        )
        self.assertEqual(total_vacancy["total_vacancy"], 2)

    def test_get_all_rooms_of_room_type_valid(self):
        rooms = RoomTypeService.get_all_rooms_of_room_type(
            room_type_id=self.room_type_1.id
        )
        self.assertEqual(rooms.count(), 2)
        room_ids = [room.id for room in rooms]
        self.assertIn(self.room1.id, room_ids)
        self.assertIn(self.room3.id, room_ids)

    def test_get_vacancy_for_each_room_of_room_type_valid(self):
        vacancy_list = RoomTypeService.get_vacancy_for_each_room_of_room_type(
            room_type_id=self.room_type_1.id
        )
        self.assertEqual(len(vacancy_list), 2)
        for vacancy in vacancy_list:
            self.assertIn("room_id", vacancy)
            self.assertIn("vacancy", vacancy)
            self.assertEqual(vacancy["vacancy"], self.room_type_1.capacity)
