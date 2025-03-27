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


class RoomTypeViewSetTestCase3(TestCase):
    def __create_user(self, username, first_name, last_name, email, phone, password):
        return AppUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
        )

    def __create_booking(
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

        self.app_user3 = self.__create_user(
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

        self.app_user2 = self.__create_user(
            "customer_user",
            "Pepita",
            "Flores",
            "customer43@example.com",
            "+34987654322",
            "password923",
        )
        self.customer = Customer.objects.create(user_id=self.app_user2.id)
        self.booking1 = self.__create_booking(
            self.customer, self.room_type, 6, 8, 450.00
        )
        self.booking2 = self.__create_booking(
            self.customer, self.room_type, 10, 12, 300.00
        )

    def test_available_room_type(self):
        start_date = date.today() + timedelta(days=2)
        end_date = start_date + timedelta(days=2)
        url = reverse("room-type-list")
        response = self.client.get(
            url,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Suite")

    def test_available_room_types(self):
        start_date = date.today() + timedelta(days=4)
        end_date = start_date + timedelta(days=1)

        url = reverse("room-type-list")
        response = self.client.get(
            url,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.room_type.id)

    def test_available_room_types_ignores_dates_without_is_available(self):
        start_date = date.today() + timedelta(days=6)
        end_date = date.today() + timedelta(days=8)
        url = reverse("room-type-list")
        response = self.client.get(
            url,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_available_room_types_no_availability(self):
        start_date = date.today() + timedelta(days=4)
        end_date = date.today() + timedelta(days=7)

        url = reverse("room-type-list")
        response = self.client.get(
            url,
            {
                "is_available": True,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
