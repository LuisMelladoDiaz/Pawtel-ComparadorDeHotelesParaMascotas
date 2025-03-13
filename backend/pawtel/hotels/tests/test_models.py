from django.core.exceptions import ValidationError
from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel


class HotelModelTest(TestCase):

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

    def test_create_valid_hotel(self):
        hotel = Hotel.objects.create(
            name="Barceló",
            address="Calle Principal 123",
            city="Madrid",
            description="Un hotel de prueba con buenas vistas.",
            hotel_owner=self.owner,
        )
        self.assertEqual(hotel.name, "Barceló")
        self.assertEqual(hotel.address, "Calle Principal 123")
        self.assertEqual(hotel.city, "Madrid")
        self.assertEqual(hotel.description, "Un hotel de prueba con buenas vistas.")
        self.assertEqual(hotel.hotel_owner, self.owner)

    def test_create_hotel_without_owner(self):
        hotel = Hotel(
            name="Barceló",
            address="Calle Principal 123",
            city="Madrid",
            description="Un hotel de prueba con buenas vistas.",
            hotel_owner=None,
        )
        with self.assertRaises(ValidationError):
            hotel.full_clean()

    def test_create_hotel_invalid_owner(self):
        invalid_python_values = ["", 123, {}, []]

        for invalid_owner in invalid_python_values:
            with self.subTest(owner=invalid_owner):
                with self.assertRaises(ValueError):
                    Hotel(
                        name="Barceló",
                        address="Calle Principal 123",
                        city="Madrid",
                        description="Un hotel de prueba con buenas vistas.",
                        hotel_owner=invalid_owner,
                    )

    def test_create_hotel_invalid_name(self):
        invalid_names = ["", None, "A" * 101]

        for name in invalid_names:
            with self.subTest(name=name):
                hotel = Hotel(
                    name=name,
                    address="Calle Principal 123",
                    city="Madrid",
                    description="Un hotel de prueba con buenas vistas.",
                    hotel_owner=self.owner,
                )
                with self.assertRaises(ValidationError):
                    hotel.full_clean()

    def test_create_hotel_invalid_address(self):
        invalid_address = ["", None, "A" * 101]

        for address in invalid_address:
            with self.subTest(address=address):
                hotel = Hotel(
                    name="Barceló",
                    address=address,
                    city="Madrid",
                    description="Un hotel de prueba con buenas vistas.",
                    hotel_owner=self.owner,
                )
                with self.assertRaises(ValidationError):
                    hotel.full_clean()

    def test_create_hotel_invalid_city(self):
        invalid_cities = ["", None, "A" * 51]

        for city in invalid_cities:
            with self.subTest(city=city):
                hotel = Hotel(
                    name="Barceló",
                    address="Calle Principal 123",
                    city=city,
                    description="Un hotel de prueba con buenas vistas.",
                    hotel_owner=self.owner,
                )
                with self.assertRaises(ValidationError):
                    hotel.full_clean()

    def test_create_hotel_invalid_description(self):
        invalid_descriptions = ["", None, "A" * 401]

        for description in invalid_descriptions:
            with self.subTest(description=description):
                hotel = Hotel(
                    name="Barceló",
                    address="Calle Principal 123",
                    city="Madrid",
                    description=description,
                    hotel_owner=self.owner,
                )
                with self.assertRaises(ValidationError):
                    hotel.full_clean()
