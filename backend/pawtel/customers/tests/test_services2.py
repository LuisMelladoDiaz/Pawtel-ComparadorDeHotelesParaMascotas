from datetime import date, timedelta

from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.customers.services import CustomerService
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType


class CustomerServiceTest2(TestCase):
    def setUp(self):
        # Crear usuario y cliente
        self.user_customer = AppUser.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            phone="+34987654321",
            password="password123",
        )
        self.customer = Customer.objects.create(user=self.user_customer)

        # Crear usuario y hotel owner
        self.user_owner = AppUser.objects.create_user(
            username="hotel_owner",
            email="owner@example.com",
            phone="+34987654322",
            password="password123",
        )
        self.hotel_owner = HotelOwner.objects.create(user=self.user_owner)

        # Crear hotel y room type
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="123 Street",
            city="Madrid",
            description="Hotel de prueba",
            hotel_owner=self.hotel_owner,
        )
        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite",
            description="Luxury suite",
            capacity=2,
            num_rooms=3,
            price_per_night=150.00,
            pet_type="DOG",
        )

        # Crear reservas para el cliente
        self.booking1 = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=450.00,
        )
        self.booking2 = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            total_price=300.00,
        )

    def test_list_bookings_of_customer(self):
        bookings = CustomerService.list_bookings_of_customer(self.customer.id)
        self.assertEqual(len(bookings), 2)

    def test_get_all_bookings_by_non_existent_customer(self):
        bookings = CustomerService.list_bookings_of_customer(999)
        self.assertEqual(len(bookings), 0)
