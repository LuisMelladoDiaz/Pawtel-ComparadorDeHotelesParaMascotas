from datetime import date, timedelta

from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.customers.services import CustomerService
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from rest_framework.exceptions import NotFound, PermissionDenied


class CustomerServiceTest2(TestCase):
    def setUp(self):
        """🔹 Configuración inicial de clientes, hoteles y reservas."""
        self.app_user_customer1 = AppUser.objects.create_user(
            username="customer1",
            first_name="Alice",
            last_name="Smith",
            email="customer1@example.com",
            phone="+34678901234",
            password="securepassword123",
        )
        self.app_user_customer2 = AppUser.objects.create_user(
            username="customer2",
            first_name="Bob",
            last_name="Johnson",
            email="customer2@example.com",
            phone="+34678901235",
            password="securepassword123",
        )

        self.customer1 = Customer.objects.create(user=self.app_user_customer1)
        self.customer2 = Customer.objects.create(user=self.app_user_customer2)

        self.hotel_owner_user = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.hotel_owner = HotelOwner.objects.create(user=self.hotel_owner_user)
        self.hotel = Hotel.objects.create(
            name="Test Hotel", is_archived=False, hotel_owner=self.hotel_owner
        )

        self.room_type = RoomType.objects.create(
            name="Deluxe Room",
            hotel=self.hotel,
            description="A luxurious room.",
            capacity=2,
            price_per_night=120.0,
            pet_type="DOG",
        )

        self.booking1 = Booking.objects.create(
            customer=self.customer1,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=7),
            total_price=1200.0,
        )

        self.booking2 = Booking.objects.create(
            customer=self.customer1,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=14),
            total_price=800.0,
        )

        self.booking3 = Booking.objects.create(
            customer=self.customer2,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=15),
            end_date=date.today() + timedelta(days=20),
            total_price=1000.0,
        )

    def test_get_all_bookings_by_customer_success(self):
        bookings = CustomerService.get_all_bookings_by_customer(
            self.customer1.id, self.app_user_customer1
        )
        self.assertEqual(len(bookings), 2)

    def test_get_all_bookings_by_customer_not_found(self):
        with self.assertRaises(NotFound):
            CustomerService.get_all_bookings_by_customer(999, self.app_user_customer1)

    def test_get_all_bookings_by_customer_permission_denied(self):
        with self.assertRaises(PermissionDenied):
            CustomerService.get_all_bookings_by_customer(
                self.customer1.id, self.app_user_customer2
            )
