from django.core.exceptions import ValidationError
from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType


class RoomTypeModelTest(TestCase):

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

    def test_create_valid_roomtype(self):
        room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite Deluxe",
            description="Una habitación lujosa con vista al mar.",
            capacity=2,
            price_per_night=150.00,
            pet_type=PetType.DOG,
        )
        self.assertEqual(room_type.name, "Suite Deluxe")
        self.assertEqual(
            room_type.description, "Una habitación lujosa con vista al mar."
        )
        self.assertEqual(room_type.capacity, 2)
        self.assertEqual(room_type.price_per_night, 150.00)
        self.assertEqual(room_type.pet_type, PetType.DOG)
        self.assertEqual(room_type.hotel, self.hotel)
        self.assertEqual(room_type.hotel.hotel_owner, self.owner)

    def test_create_roomtype_without_hotel(self):
        with self.assertRaises(ValidationError):
            RoomType(
                hotel=None,
                name="Suite Deluxe",
                description="Una habitación lujosa con vista al mar.",
                capacity=2,
                price_per_night=150.00,
                pet_type=PetType.DOG,
            ).full_clean()

    def test_create_roomtype_invalid_name(self):
        invalid_names = ["", None, "A" * 51]
        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ValidationError):
                    RoomType(
                        hotel=self.hotel,
                        name=name,
                        description="Una habitación lujosa con vista al mar.",
                        capacity=2,
                        price_per_night=150.00,
                        pet_type=PetType.DOG,
                    ).full_clean()

    def test_create_roomtype_invalid_description(self):
        invalid_descriptions = ["", None, "A" * 301]
        for description in invalid_descriptions:
            with self.subTest(description=description):
                with self.assertRaises(ValidationError):
                    RoomType(
                        hotel=self.hotel,
                        name="Suite Deluxe",
                        description=description,
                        capacity=2,
                        price_per_night=150.00,
                        pet_type=PetType.DOG,
                    ).full_clean()

    def test_create_roomtype_invalid_capacity(self):
        invalid_capacities = [0, -1, None]
        for capacity in invalid_capacities:
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValidationError):
                    RoomType(
                        hotel=self.hotel,
                        name="Suite Deluxe",
                        description="Una habitación lujosa con vista al mar.",
                        capacity=capacity,
                        price_per_night=150.00,
                        pet_type=PetType.DOG,
                    ).full_clean()

    def test_create_roomtype_invalid_price(self):
        invalid_prices = [0, -10.00, None]
        for price in invalid_prices:
            with self.subTest(price=price):
                with self.assertRaises(ValidationError):
                    RoomType(
                        hotel=self.hotel,
                        name="Suite Deluxe",
                        description="Una habitación lujosa con vista al mar.",
                        capacity=2,
                        price_per_night=price,
                        pet_type=PetType.DOG,
                    ).full_clean()

    def test_create_roomtype_invalid_pet_type(self):
        invalid_pet_types = ["", None, "FISH"]
        for pet_type in invalid_pet_types:
            with self.subTest(pet_type=pet_type):
                with self.assertRaises(ValidationError):
                    RoomType(
                        hotel=self.hotel,
                        name="Suite Deluxe",
                        description="Una habitación lujosa con vista al mar.",
                        capacity=2,
                        price_per_night=150.00,
                        pet_type=pet_type,
                    ).full_clean()
