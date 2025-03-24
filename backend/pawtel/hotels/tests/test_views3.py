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
    def create_user(self, username, first_name, last_name, email, phone, password):
        return AppUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
        )

    def create_booking(
        self, customer, room_type, start_offset, end_offset, total_price
    ):
        today = date.today()
        return Booking.objects.create(
            customer=customer,
            room_type=room_type,
            start_date=today + timedelta(days=start_offset),
            end_date=today + timedelta(days=end_offset),
            total_price=total_price,
        )

    def setUp(self):
        self.client = APIClient()

        self.app_user3 = self.create_user(
            "hotel_owner2",
            "Johnttt",
            "Dotte",
            "owner32@example.com",
            "+34987654444",
            "password456",
        )
        self.client.force_authenticate(user=self.app_user3)

        hotel_owner = HotelOwner.objects.create(user_id=self.app_user3.id)
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="123 Street",
            city="Madrid",
            description="Hotel de prueba",
            hotel_owner=hotel_owner,
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite",
            description="Luxury suite",
            capacity=1,
            num_rooms=1,
            price_per_night=150.00,
            pet_type="DOG",
        )

        self.app_user2 = self.create_user(
            "customer_user",
            "Pepita",
            "Flores",
            "customer43@example.com",
            "+34987654322",
            "password923",
        )
        self.customer = Customer.objects.create(user_id=self.app_user2.id)
        self.booking1 = self.create_booking(self.customer, self.room_type, 6, 8, 450.00)
        self.booking2 = self.create_booking(
            self.customer, self.room_type, 10, 12, 300.00
        )


class TestNuevasRutasHotel(HotelViewSetTestCase2):
    def test_available_hotels_con_room_type_disponible(self):
        start_date = date.today() + timedelta(days=2)
        end_date = start_date + timedelta(days=2)
        url = reverse("hotel-available_hotels")
        response = self.client.get(
            url,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], "Madrid")

    def test_available_room_types_con_disponibilidad(self):
        start_date = date.today() + timedelta(days=4)
        end_date = start_date + timedelta(days=1)

        url = reverse("hotel-available_room_types", kwargs={"pk": self.hotel.id})
        response = self.client.get(
            url,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.room_type.id)

    def test_available_hotels_sin_room_type_disponible(self):
        start_date = date.today() + timedelta(days=6)
        end_date = date.today() + timedelta(days=8)
        url = reverse("hotel-available_hotels")
        response = self.client.get(
            url,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_available_room_types_sin_disponibilidad(self):
        start_date = date.today() + timedelta(days=4)
        end_date = date.today() + timedelta(days=7)

        url = reverse("hotel-available_room_types", kwargs={"pk": self.hotel.id})
        response = self.client.get(
            url,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
