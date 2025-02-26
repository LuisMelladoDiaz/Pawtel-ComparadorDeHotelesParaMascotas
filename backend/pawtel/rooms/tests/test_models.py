from django.test import TestCase
from rooms.models import Room
from roomTypes.models import RoomType
from hotels.models import Hotel
from django.core.exceptions import ValidationError

class RoomModelTest(TestCase):

    def setUp(self):
        """Configuración inicial: Crear un hotel y un RoomType válidos"""
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="Calle Principal 123",
            city="Madrid",
            description="Un hotel de prueba."
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite Deluxe",
            description="Una habitación lujosa con vista al mar.",
            capacity=2,
            price_per_night=150.00,
            pet_type="DOG"
        )

    def test_create_valid_room(self):
        """Prueba la creación de un Room válido"""
        room = Room.objects.create(
            name="Habitación 101",
            room_type=self.room_type
        )
        self.assertEqual(room.name, "Habitación 101")
        self.assertEqual(room.room_type, self.room_type)

    def test_create_room_invalid_name(self):
        """Intenta crear un Room sin nombre"""
        with self.assertRaises(ValidationError):
            room = Room.objects.create(
                name="",  # Nombre vacío
                room_type=self.room_type
            )
            room.full_clean()


    def test_create_room_invalid_room_type(self):
        """Intenta crear un Room sin un RoomType asignado (ForeignKey required)"""
        with self.assertRaises(ValidationError):
            room = Room.objects.create(
                name="Habitación sin Tipo",
                room_type=None  #No puede ser null
            )
            room.full_clean()