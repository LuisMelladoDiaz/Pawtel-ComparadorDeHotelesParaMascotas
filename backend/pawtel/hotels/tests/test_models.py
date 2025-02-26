from django.test import TestCase
from hotels.models import Hotel
from django.core.exceptions import ValidationError

class HotelModelTest(TestCase):

    def test_create_valid_hotel(self):
        """creación de un Hotel válido"""
        hotel = Hotel.objects.create(
            name="Barceló",
            address="Calle Principal 123",
            city="Madrid",
            description="Un hotel de prueba con buenas vistas."
        )
        self.assertEqual(hotel.name, "Barceló")
        self.assertEqual(hotel.address, "Calle Principal 123")
        self.assertEqual(hotel.city, "Madrid")
        self.assertEqual(hotel.description, "Un hotel de prueba con buenas vistas.")

    def test_create_hotel_invalid_name(self):
        """crear un Hotel sin nombre"""
        with self.assertRaises(ValidationError):
            hotel = Hotel.objects.create(
                name="",
                address="Calle Principal 123",
                city="Madrid",
                description="Un hotel de prueba."
            )
            hotel.full_clean()


    def test_create_hotel_invalid_address(self):
        """crear un Hotel sin dirección"""
        with self.assertRaises(ValidationError):
            hotel = Hotel.objects.create(
                name="Hotel Sirena",
                address="",
                city="Sevilla",
                description="Hotel muy chill"
            )
            hotel.full_clean()

    def test_create_hotel_invalid_city(self):
        """crear un Hotel sin ciudad"""
        with self.assertRaises(ValidationError):
            hotel = Hotel.objects.create(
                name="Hotel Sevilla",
                address="Avenida del Mar 22",
                city="",
                description="Hotel de lujo"
            )
            hotel.full_clean()

    def test_create_hotel_invalid_description(self):
        """crear un Hotel sin descripción"""
        with self.assertRaises(ValidationError):
            hotel = Hotel.objects.create(
                name="Hotel 3 lunas",
                address="Calle de la Luna 5",
                city="Valencia",
                description=""
            )
            hotel.full_clean()