import json
from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils.timezone import now
from pawtel.app_users.models import AppUser
from pawtel.booking_holds.models import BookingHold
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

        self.app_user_customer1 = AppUser.objects.create_user(
            username="customer_maria",
            first_name="María",
            last_name="González",
            email="maria_g@example.com",
            phone="+34987654101",
            password="maria_password",
        )

        self.app_user_customer2 = AppUser.objects.create_user(
            username="customer_pedro",
            first_name="Pedro",
            last_name="Martínez",
            email="pedro_m@example.com",
            phone="+34987654102",
            password="pedro_password",
        )

        self.app_user_hotel_owner1 = AppUser.objects.create_user(
            username="hotelowner_owen",
            first_name="Owen",
            last_name="Smith",
            email="owen_h@example.com",
            phone="+34987754111",
            password="owen_password",
        )

        self.app_user_hotel_owner2 = AppUser.objects.create_user(
            username="hotelowner_lucia",
            first_name="Lucía",
            last_name="Fernández",
            email="lucia_h@example.com",
            phone="+34987254112",
            password="lucia_password",
        )

        self.customer1 = Customer.objects.create(user=self.app_user_customer1)
        self.customer2 = Customer.objects.create(user=self.app_user_customer2)
        self.hotel_owner1 = HotelOwner.objects.create(user=self.app_user_hotel_owner1)
        self.hotel_owner2 = HotelOwner.objects.create(user=self.app_user_hotel_owner2)

        self.hotel1 = Hotel.objects.create(
            name="Hotel Sol y Playa",
            address="Avenida del Mar 123",
            city="Madrid",
            description="Hotel con vista al mar y piscina.",
            hotel_owner=self.hotel_owner1,
        )

        self.hotel2 = Hotel.objects.create(
            name="Hotel Montaña Azul",
            address="Calle de la Sierra 45",
            city="Barcelona",
            description="Hotel en la montaña con spa y actividades al aire libre.",
            hotel_owner=self.hotel_owner2,
        )

        self.room_type1 = RoomType.objects.create(
            hotel=self.hotel1,
            name="Suite Familiar",
            description="Habitación con terraza y vista al mar.",
            capacity=4,
            price_per_night=220.00,
            pet_type="DOG",
        )

        self.room_type2 = RoomType.objects.create(
            hotel=self.hotel2,
            name="Habitación Doble Premium",
            description="Habitación de lujo con servicio de mayordomo.",
            capacity=2,
            price_per_night=280.00,
            pet_type="CAT",
        )

        self.booking1 = Booking.objects.create(
            customer=self.customer1,
            room_type=self.room_type1,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=660.00,
        )

        self.booking2 = Booking.objects.create(
            customer=self.customer2,
            room_type=self.room_type2,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=7),
            total_price=1120.00,
        )

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
        self.assertEqual(len(bookings), 3)

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

    def test_booking_hold_deleted_on_booking_complete(self):
        booking_hold = BookingHold.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            hold_expires_at=now() + timedelta(minutes=15),
            booking_start_date=date.today() + timedelta(days=2),
            booking_end_date=date.today() + timedelta(days=5),
        )

        start_date = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
        end_date = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
        booking_data = {
            "room_type": self.room_type.id,
            "start_date": start_date,
            "end_date": end_date,
            "customer": self.customer.id,
            "total_price": 600.00,
        }

        FakeObject = type(
            "FakeObject", (), {"metadata": {"booking": json.dumps(booking_data)}}
        )
        FakeData = type("FakeData", (), {"object": FakeObject()})
        FakeEvent = type("FakeEvent", (), {})()
        FakeEvent.type = "checkout.session.completed"
        FakeEvent.data = FakeData()

        self.assertTrue(
            BookingHold.objects.filter(
                customer=self.customer, room_type=self.room_type
            ).exists()
        )

        with patch(
            "pawtel.bookings.services.stripe.Webhook.construct_event",
            return_value=FakeEvent,
        ):
            response = BookingService.stripe_response_manager(
                b"dummy_payload", "dummy_sig"
            )
            self.assertEqual(response.status_code, 200)

        self.assertFalse(
            BookingHold.objects.filter(
                customer=self.customer, room_type=self.room_type
            ).exists()
        )
