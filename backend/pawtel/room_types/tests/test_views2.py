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


class TestRoomTypeViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.app_user_owner = AppUser.objects.create_user(
            username="hotel_owner",
            email="owner@example.com",
            phone="+34123456789",
            password="securepass",
        )
        self.hotel_owner = HotelOwner.objects.create(
            user=self.app_user_owner, is_approved=True
        )
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
            description="Habitación de lujo",
            capacity=2,
            num_rooms=3,
            price_per_night=100.00,
            pet_type="DOG",
        )

        self.app_user_customer = AppUser.objects.create_user(
            username="customer",
            email="customer@example.com",
            phone="+34987654321",
            password="securepass",
        )
        self.customer = Customer.objects.create(user=self.app_user_customer)

        self.client.force_authenticate(user=self.app_user_customer)

    # Tests --------------------------------------------------------------------

    def test_is_room_type_available(self):
        url = reverse(
            "room-type-is_room_type_available", kwargs={"pk": self.room_type.id}
        )
        response = self.client.get(
            url,
            {
                "start_date": str(date.today()),
                "end_date": str(date.today() + timedelta(days=2)),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get("is_available"))

    def test_is_room_type_not_available(self):
        for _ in range(self.room_type.num_rooms * self.room_type.capacity):
            Booking.objects.create(
                customer=self.customer,
                room_type=self.room_type,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=2),
                total_price=300.00,
            )

        url = reverse(
            "room-type-is_room_type_available", kwargs={"pk": self.room_type.id}
        )
        response = self.client.get(
            url,
            {
                "start_date": str(date.today()),
                "end_date": str(date.today() + timedelta(days=2)),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json().get("is_available"))

    def test_room_type_not_available_only_one_day_occupied(self):
        for _ in range(self.room_type.num_rooms * self.room_type.capacity):
            Booking.objects.create(
                customer=self.customer,
                room_type=self.room_type,
                start_date=date.today() + timedelta(days=3),
                end_date=date.today() + timedelta(days=3),
                total_price=300.00,
            )

        url = reverse(
            "room-type-is_room_type_available", kwargs={"pk": self.room_type.id}
        )
        response = self.client.get(
            url,
            {
                "start_date": str(date.today()),
                "end_date": str(date.today() + timedelta(days=5)),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json().get("is_available"))

    def test_is_room_type_missing_dates(self):
        url = reverse(
            "room-type-is_room_type_available", kwargs={"pk": self.room_type.id}
        )
        response = self.client.get(url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "La fecha inicial y la fecha final son obligatorias.",
            response.json().get("detail"),
        )
