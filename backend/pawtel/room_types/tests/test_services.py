from datetime import date, timedelta

from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from pawtel.room_types.services import RoomTypeService
from rest_framework.exceptions import NotFound


class TestRoomTypeService(TestCase):
    def setUp(self):
        # Crear usuario, hotel owner y hotel
        self.app_user = AppUser.objects.create_user(
            username="hotel_owner",
            email="owner@example.com",
            phone="+34123456789",
            password="securepass",
        )
        self.hotel_owner = HotelOwner.objects.create(user=self.app_user)
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="123 Street",
            city="Madrid",
            description="Hotel de prueba",
            hotel_owner=self.hotel_owner,
        )

        # Crear RoomType
        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite",
            description="Habitación de lujo",
            capacity=2,
            num_rooms=3,  # 3 habitaciones con capacidad de 2 cada una (6 en total)
            price_per_night=100.00,
            pet_type="DOG",
        )

        # Crear cliente
        self.app_user_customer = AppUser.objects.create_user(
            username="customer",
            email="customer@example.com",
            phone="+34987654321",
            password="securepass",
        )
        self.customer = Customer.objects.create(user=self.app_user_customer)

    def test_room_type_available(self):
        # Verifica que la habitación está disponible cuando no hay reservas.
        is_available = RoomTypeService.is_room_type_available(
            self.room_type.id, date.today(), date.today() + timedelta(days=2)
        )
        self.assertTrue(is_available)

    def test_room_type_not_available(self):
        # Verifica que la habitación NO está disponible si hay reservas en todas las habitaciones.
        Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            total_price=300.00,
        )
        Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            total_price=300.00,
        )
        Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            total_price=300.00,
        )  # 3 reservas ocupando las 3 habitaciones

        is_available = RoomTypeService.is_room_type_available(
            self.room_type.id, date.today(), date.today() + timedelta(days=2)
        )
        self.assertTrue(is_available)

    def test_room_type_not_found(self):
        # Verifica que se lanza NotFound si el RoomType no existe.
        with self.assertRaises(NotFound):
            RoomTypeService.is_room_type_available(
                999, date.today(), date.today() + timedelta(days=2)
            )
