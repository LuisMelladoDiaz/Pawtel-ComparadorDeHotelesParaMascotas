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

        # Crear usuario y hotel owner
        self.app_user = AppUser.objects.create_user(
            username="hotel_owner",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="password123",
        )
        self.client.force_authenticate(user=self.app_user)
        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user.id)

        # Crear hotel
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="123 Street",
            city="Madrid",
            description="Hotel de prueba",
            hotel_owner=self.hotel_owner,
        )

        # Crear RoomType
        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite",
            description="Luxury suite",
            capacity=2,
            num_rooms=3,
            price_per_night=150.00,
            pet_type="DOG",
        )

        # Crear usuario cliente
        self.app_user2 = AppUser.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            phone="+34987654322",
            password="password123",
        )
        self.customer = Customer.objects.create(user_id=self.app_user2.id)

        # Crear reservas para el hotel
        self.booking1 = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=450.00,
        )
        self.booking2 = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            total_price=300.00,
        )

    def test_get_all_bookings_by_hotel_explicit(self):
        """Verifica que el endpoint devuelve todas las reservas de un hotel."""
        self.client.force_authenticate(user=self.app_user)
        self.client.force_authenticate(user=self.app_user2)
        url = reverse(
            "hotel-get_all_bookings_by_hotel_explicit", kwargs={"pk": self.hotel.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Debe devolver dos reservas
