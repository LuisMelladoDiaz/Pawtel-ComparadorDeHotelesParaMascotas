from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from rest_framework import status
from rest_framework.test import APIClient


class HotelViewSetTestCase2(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app_user_owner1 = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner1@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.client.force_authenticate(user=self.app_user_owner1)
        self.app_user_owner2 = AppUser.objects.create_user(
            username="hotelowner2",
            first_name="Alice",
            last_name="Smith",
            email="owner2@example.com",
            phone="+34987654322",
            password="securepassword123",
        )
        self.client.force_authenticate(user=self.app_user_owner2)

        # Create Hotel Owners
        self.hotel_owner1 = HotelOwner.objects.create(user_id=self.app_user_owner1.id)
        self.hotel_owner2 = HotelOwner.objects.create(user_id=self.app_user_owner2.id)

        # Create Hotels
        self.hotel1 = Hotel.objects.create(
            name="Test Hotel",
            is_archived=False,
            hotel_owner=self.hotel_owner1,
        )

        self.hotel2 = Hotel.objects.create(
            name="Hotel Luna Azul",
            is_archived=False,
            hotel_owner=self.hotel_owner2,
        )

        # Create Room Types
        self.room_type1 = RoomType.objects.create(
            name="Single",
            hotel=self.hotel1,
            description="A cozy single room.",
            capacity=1,
            price_per_night=50.0,
            pet_type="DOG",
        )

        self.room_type2 = RoomType.objects.create(
            name="Double",
            hotel=self.hotel1,
            description="A spacious double room.",
            capacity=2,
            price_per_night=75.0,
            pet_type="CAT",
        )

        # Create Customers (NEW)
        self.customer1 = Customer.objects.create(user=self.app_user_owner1)
        self.customer2 = Customer.objects.create(user=self.app_user_owner2)

        # Create Bookings (FIXED)
        self.booking1 = Booking.objects.create(
            customer=self.customer1,  # FIX: Use Customer instance
            room_type=self.room_type1,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=7),
            total_price=400.00,
        )

        self.booking2 = Booking.objects.create(
            customer=self.customer2,  # FIX: Use Customer instance
            room_type=self.room_type2,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=10),
            total_price=1000.00,
        )


def test_get_all_bookings_by_hotel_implicit(self):
    url = reverse("hotel-get_all_bookings_by_hotel_implicit")
    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]["id"], self.booking1.id)
