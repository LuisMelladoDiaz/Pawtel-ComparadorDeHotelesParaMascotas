from django.test import TestCase
from roomTypes.models import RoomType, PetType
from hotels.models import Hotel
from django.core.exceptions import ValidationError

class RoomTypeModelTest(TestCase):

    def setUp(self):
        """Crear un hotel válido para asociarlo a RoomType"""
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="Calle Principal 123",
            city="Madrid",
            description="Un hotel de prueba."
        )

    def test_create_valid_roomtype(self):
        """Prueba la creación de un RoomType válido"""
        room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite Deluxe",
            description="Una habitación lujosa con vista al mar.",
            capacity=2,
            price_per_night=150.00,
            pet_type=PetType.DOG
        )
        self.assertEqual(room_type.name, "Suite Deluxe")
        self.assertEqual(room_type.description, "Una habitación lujosa con vista al mar.")
        self.assertEqual(room_type.capacity, 2)
        self.assertEqual(room_type.price_per_night, 150.00)
        self.assertEqual(room_type.pet_type, PetType.DOG)

    def test_create_roomtype_invalid_name(self):
        """Intenta crear un RoomType sin nombre"""
        with self.assertRaises(ValidationError):
            room_type = RoomType.objects.create(
                hotel=self.hotel,
                name="",
                description="Habitación sin nombre.",
                capacity=2,
                price_per_night=100.00,
                pet_type=PetType.CAT
            )
            room_type.full_clean()


    def test_create_roomtype_invalid_description(self):
        """Intenta crear un RoomType sin descripción """
        with self.assertRaises(ValidationError):
            room_type = RoomType.objects.create(
                hotel=self.hotel,
                name="Habitación Económica",
                description="",
                capacity=1,
                price_per_night=50.00,
                pet_type=PetType.ANY
            )
            room_type.full_clean()

    def test_create_roomtype_invalid_capacity(self):
        """Intenta crear un RoomType con capacidad fuera de rango"""
        with self.assertRaises(ValidationError):
            room_type = RoomType.objects.create(
                hotel=self.hotel,
                name="Habitación Triple",
                description="Habitación espaciosa.",
                capacity=0,  # Capacidad inválida (mínimo 1)
                price_per_night=120.00,
                pet_type=PetType.DOG
            )
            room_type.full_clean()

    def test_create_roomtype_invalid_price(self):
        """Intenta crear un RoomType con precio fuera de rango"""
        with self.assertRaises(ValidationError):
            room_type = RoomType.objects.create(
                hotel=self.hotel,
                name="Habitación VIP",
                description="Habitación con jacuzzi.",
                capacity=2,
                price_per_night=-10.00,  #Precio inválido (mínimo 1)
                pet_type=PetType.CAT
            )
            room_type.full_clean()

    def test_create_roomtype_invalid_pet_type(self):
        """Intenta crear un RoomType con un tipo de mascota no válido"""
        with self.assertRaises(ValueError):  # Se espera un ValueError si elige un valor no permitido
            room_type = RoomType.objects.create(
                hotel=self.hotel,
                name="Habitación sin mascotas",
                description="No se permiten mascotas.",
                capacity=2,
                price_per_night=90.00,
                pet_type="FISH"  # Tipo de mascota no definido en PetType
            )
            room_type.full_clean()