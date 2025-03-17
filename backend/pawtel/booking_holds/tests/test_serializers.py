from datetime import date

from django.test import TestCase
from django.utils.timezone import now, timedelta
from pawtel.app_users.models import AppUser
from pawtel.booking_holds.models import BookingHold
from pawtel.booking_holds.serializers import BookingHoldSerializer
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType


class BookingHoldSerializerTest(TestCase):

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
            name="Test Hotel",
            address="123 Test Street",
            city="Madrid",
            description="A test hotel",
            hotel_owner=self.owner,
        )
        self.room_type = RoomType.objects.create(
            name="Deluxe Room",
            description="A luxury room",
            capacity=2,
            num_rooms=10,
            price_per_night=200.00,
            pet_type=PetType.DOG,
            hotel=self.hotel,
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

        self.in_ten_minutes = now() + timedelta(minutes=10)
        self.in_two_days = date.today() + timedelta(days=2)
        self.in_four_days = date.today() + timedelta(days=4)

        self.valid_booking_hold = BookingHold.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            hold_expires_at=self.in_ten_minutes,
            booking_start_date=self.in_two_days,
            booking_end_date=self.in_four_days,
        )
        self.valid_data = {
            "customer": self.customer.id,
            "room_type": self.room_type.id,
            "hold_expires_at": self.in_ten_minutes,
            "booking_start_date": self.in_two_days,
            "booking_end_date": self.in_four_days,
        }

    def test_valid_booking_hold_serialization(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = BookingHoldSerializer(self.valid_data, context=context)
        self.assertEqual(serializer.data["customer"], self.valid_data.get("customer"))
        self.assertEqual(serializer.data["room_type"], self.valid_data.get("room_type"))
        self.assertIn("hold_expires_at", serializer.data)
        self.assertIn("is_expired", serializer.data)

    def test_valid_booking_hold_serialization(self):
        context = {"request": type("Request", (), {"method": "GET"})}
        serializer = BookingHoldSerializer(self.valid_booking_hold, context=context)
        self.assertEqual(serializer.data["customer"], self.valid_data.get("customer"))
        self.assertEqual(serializer.data["room_type"], self.valid_data.get("room_type"))
        self.assertIn("hold_expires_at", serializer.data)
        self.assertIn("is_expired", serializer.data)

    def test_missing_customer_fails(self):
        data = {
            "room_type": self.room_type.id,
        }
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = BookingHoldSerializer(data=data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer", serializer.errors)

    def test_missing_room_type_fails(self):
        data = {
            "customer": self.customer.id,
        }
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = BookingHoldSerializer(data=data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("room_type", serializer.errors)

    def test_ignore_extra_fields(self):
        data = self.valid_data
        data["extra_field"] = "This should not be here"
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = BookingHoldSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("extra_field", serializer.validated_data)
