from django.test import TestCase
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied, NotFound
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.hotels.models import Hotel
from pawtel.hotel_owners.models import HotelOwner
from pawtel.room_types.models import RoomType
from pawtel.bookings.models import Booking
from pawtel.bookings.services import BookingService
from pawtel.customers.services import CustomerService


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

    #CREATE Method Tests ----------------------------------------------

    def test_create_valid_booking(self):
        """✅ Servicio crea una reserva correctamente."""
        request_mock = type("Request", (), {"user": self.app_user_customer})
        booking = BookingService.create_booking(request_mock, self.booking_data)

        self.assertIsNotNone(booking.id)
        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.room_type, self.room_type)
        self.assertEqual(booking.total_price, 600.00)  # 3 nights * 200€

    def test_create_booking_overlapping(self):
        request_mock = type("Request", (), {"user": self.app_user_customer})

        # Create first booking
        BookingService.create_booking(request_mock, self.booking_data)

        #Try create another booking superpuesta
        with self.assertRaises(ValidationError):
            BookingService.create_booking(request_mock, self.booking_data)

    def test_create_booking_invalid_end_date(self):
        #end_date must be after start_date
        request_mock = type("Request", (), {"user": self.app_user_customer})
        invalid_data = self.booking_data.copy()
        invalid_data["end_date"] = invalid_data["start_date"]  #  It can´t be the same

        with self.assertRaises(ValidationError):
            BookingService.create_booking(request_mock, invalid_data)

    def test_create_booking_invalid_room_type(self):
        request_mock = type("Request", (), {"user": self.app_user_customer})
        invalid_data = self.booking_data.copy()
        invalid_data["room_type"] = 999  #RoomType doesn´t exist

        with self.assertRaises(NotFound):
            BookingService.create_booking(request_mock, invalid_data)

    # GET Method Tests 

    def test_list_bookings(self):
        request_mock = type("Request", (), {"user": self.app_user_customer})
        BookingService.create_booking(request_mock, self.booking_data)

        bookings = BookingService.list_bookings()
        self.assertEqual(len(bookings), 1)

    def test_retrieve_booking_valid(self):
        request_mock = type("Request", (), {"user": self.app_user_customer})
        booking = BookingService.create_booking(request_mock, self.booking_data)

        retrieved_booking = BookingService.retrieve_booking(booking.id)
        self.assertEqual(retrieved_booking.id, booking.id)

    def test_retrieve_booking_not_found(self):
        with self.assertRaises(NotFound):
            BookingService.retrieve_booking(999)  # Doesn´t exist


