from django.core.exceptions import ValidationError
from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room


class RoomModelTest(TestCase):

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
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="Calle Principal 123",
            city="Madrid",
            description="Un hotel de prueba.",
            hotel_owner=self.owner,
        )
        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite Deluxe",
            description="Una habitación lujosa con vista al mar.",
            capacity=2,
            price_per_night=150.00,
            pet_type="DOG",
        )

    def test_create_valid_room(self):
        room = Room.objects.create(name="Habitación 101", room_type=self.room_type)
        self.assertEqual(room.name, "Habitación 101")
        self.assertEqual(room.room_type, self.room_type)
        self.assertEqual(room.room_type.hotel, self.hotel)
        self.assertEqual(room.room_type.hotel.hotel_owner, self.owner)

    def test_create_room_invalid_name(self):
        invalid_names = ["", None, "A" * 51]

        for name in invalid_names:
            with self.subTest(name=name):
                room = Room(name=name, room_type=self.room_type)
                with self.assertRaises(ValidationError):
                    room.full_clean()

    def test_create_room_without_room_type(self):
        room = Room(name="Habitación sin Tipo", room_type=None)
        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_create_room_invalid_room_type(self):
        invalid_room_types = ["", 123, {}, []]

        for room_type in invalid_room_types:
            with self.subTest(room_type=room_type):
                with self.assertRaises(ValueError):
                    Room(name="Habitación 102", room_type=room_type)

    def test_create_multiple_rooms_with_different_room_types(self):
        another_room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite Presidencial",
            description="La mejor habitación del hotel.",
            capacity=3,
            price_per_night=300.00,
            pet_type="MIXED",
        )

        room1 = Room.objects.create(name="Habitación 101", room_type=self.room_type)
        room2 = Room.objects.create(name="Habitación 102", room_type=another_room_type)

        self.assertNotEqual(room1.room_type, room2.room_type)
        self.assertEqual(room1.room_type.hotel, room2.room_type.hotel)
