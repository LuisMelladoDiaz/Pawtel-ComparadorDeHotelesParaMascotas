from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType


class BookingModelTest(TestCase):

    def setUp(self):
        self.app_user_customer = AppUser.objects.create_user(
            username="customer10",
            first_name="Pepa",
            last_name="Johnson",
            email="pepa@example.com",
            phone="+34987654333",
            password="chocolate",
        )

        self.app_user_hotel_owner = AppUser.objects.create_user(
            username="hotelowner10",
            first_name="Carlos",
            last_name="Gomez",
            email="carlos@example.com",
            phone="+34987654334",
            password="hotelpassword",
        )

        self.customer = Customer.objects.create(user=self.app_user_customer)
        self.hotel_owner = HotelOwner.objects.create(user=self.app_user_hotel_owner)

        self.hotel = Hotel.objects.create(
            name="Barcelo Sevilla",
            address="Calle Betis",
            city="Barcelona",
            description="Un hotel exclusivo",
            hotel_owner=self.hotel_owner,
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite Ejecutiva",
            description="Habitación con vista al mar.",
            capacity=2,
            price_per_night=200.00,
            pet_type="DOG",
        )

    def test_create_valid_booking(self):
        booking = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=6),
            total_price=600.00,
            use_paw_points=True,
            discount=20,
        )
        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.room_type, self.room_type)
        self.assertEqual(booking.total_price, 600.00)
        self.assertEqual((booking.end_date - booking.start_date).days, 3)
        self.assertTrue(booking.use_paw_points)
        self.assertEqual(booking.discount, 20)

    def test_create_booking_invalid_start_date(self):
        with self.assertRaises(ValidationError):
            booking = Booking(
                customer=self.customer,
                room_type=self.room_type,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=3),
                total_price=600.00,
            )
            booking.full_clean()

    def test_create_booking_invalid_end_date(self):
        with self.assertRaises(ValidationError):
            booking = Booking(
                customer=self.customer,
                room_type=self.room_type,
                start_date=date.today() + timedelta(days=5),
                end_date=date.today() + timedelta(days=3),
                total_price=600.00,
            )
            booking.full_clean()

    def test_create_booking_invalid_price(self):
        invalid_prices = [-1, 0, None, "A"]
        for price in invalid_prices:
            with self.subTest(price=price):
                with self.assertRaises(ValidationError):
                    booking = Booking(
                        customer=self.customer,
                        room_type=self.room_type,
                        start_date=date.today() + timedelta(days=3),
                        end_date=date.today() + timedelta(days=6),
                        total_price=price,
                    )
                    booking.full_clean()

    def test_create_booking_invalid_discount(self):
        invalid_discounts = [-1, None, "A"]
        for discount in invalid_discounts:
            with self.subTest(discount=discount):
                with self.assertRaises(ValidationError):
                    booking = Booking(
                        customer=self.customer,
                        room_type=self.room_type,
                        start_date=date.today() + timedelta(days=3),
                        end_date=date.today() + timedelta(days=6),
                        total_price=0.00,
                        discount=discount,
                    )
                    booking.full_clean()
