from datetime import date, timedelta

from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.bookings.services import BookingService
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from rest_framework.exceptions import NotFound


class BookingServiceTest(TestCase):

    def setUp(self):
        self.app_user_customer = AppUser.objects.create_user(
            username="customer20",
            first_name="María",
            last_name="Johnson",
            email="maria@example.com",
            phone="+34987654111",
            password="galletasmaria",
        )
        self.app_user_hotel_owner = AppUser.objects.create_user(
            username="hotelowner20",
            first_name="Owen",
            last_name="Michael",
            email="miky@example.com",
            phone="+34987654444",
            password="balondeoro",
        )

        self.customer = Customer.objects.create(user=self.app_user_customer)
        self.hotel_owner = HotelOwner.objects.create(user=self.app_user_hotel_owner)

        self.hotel = Hotel.objects.create(
            name="Hotel discordia",
            address="Calle Sevilla",
            city="Madrid",
            description="Un hotel 5 estrellas",
            hotel_owner=self.hotel_owner,
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite royale",
            description="Habitación con vistas a la montaña.",
            capacity=2,
            price_per_night=200.00,
            pet_type="DOG",
        )

        self.booking_data = {
            "room_type": self.room_type.id,
            "start_date": date.today() + timedelta(days=2),
            "end_date": date.today() + timedelta(days=5),
        }

    # GET Method Tests

    def test_list_bookings(self):
        Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=600.00,
        )

        bookings = BookingService.list_bookings()
        self.assertEqual(len(bookings), 1)

    def test_retrieve_booking_valid(self):
        booking = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=600.00,
        )

        retrieved_booking = BookingService.retrieve_booking(booking.id)
        self.assertEqual(retrieved_booking.id, booking.id)

    def test_retrieve_booking_not_found(self):
        with self.assertRaises(NotFound):
            BookingService.retrieve_booking(999)  # It does not exist
