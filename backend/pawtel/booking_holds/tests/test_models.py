from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now, timedelta
from pawtel.app_users.models import AppUser
from pawtel.booking_holds.models import BookingHold
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType


class BookingHoldModelTest(TestCase):

    def setUp(self):
        self.app_user_owner = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.owner = HotelOwner.objects.create(user_id=self.app_user_owner.id)
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="Calle Principal 123",
            city="Madrid",
            description="Un hotel de prueba.",
            hotel_owner=self.owner,
        )
        self.room_type = RoomType.objects.create(
            name="Suite Deluxe",
            description="Una habitación lujosa con vista al mar.",
            capacity=2,
            num_rooms=10,
            price_per_night=150.00,
            pet_type=PetType.DOG,
            hotel_id=self.hotel.id,
        )
        self.app_user_customer = AppUser.objects.create_user(
            username="customer1",
            first_name="Jane",
            last_name="Doe",
            email="customer@example.com",
            phone="+34123456789",
            password="securepassword123",
        )
        self.customer = Customer.objects.create(user_id=self.app_user_customer.id)

    def test_create_valid_booking_hold(self):
        booking_hold = BookingHold.objects.create(
            customer=self.customer, room_type=self.room_type
        )
        self.assertEqual(booking_hold.customer, self.customer)
        self.assertEqual(booking_hold.room_type, self.room_type)
        self.assertTrue(booking_hold.hold_expires_at > now())

    def test_hold_expiry_function(self):
        booking_hold = BookingHold.objects.create(
            customer=self.customer, room_type=self.room_type
        )
        self.assertFalse(booking_hold.is_expired())
        booking_hold.hold_expires_at = now() - timedelta(minutes=1)
        self.assertTrue(booking_hold.is_expired())

    def test_create_booking_hold_without_customer(self):
        booking_hold = BookingHold(customer=None, room_type=self.room_type)
        with self.assertRaises(ValidationError):
            booking_hold.full_clean()

    def test_create_booking_hold_without_room_type(self):
        booking_hold = BookingHold(customer=self.customer, room_type=None)
        with self.assertRaises(ValidationError):
            booking_hold.full_clean()

    def test_invalid_hold_expires_at(self):
        invalid_dates = [None, now() - timedelta(days=1)]
        for date in invalid_dates:
            with self.subTest(hold_expires_at=date):
                booking_hold = BookingHold(
                    customer=self.customer,
                    room_type=self.room_type,
                    hold_expires_at=date,
                )
                with self.assertRaises(ValidationError):
                    booking_hold.full_clean()
