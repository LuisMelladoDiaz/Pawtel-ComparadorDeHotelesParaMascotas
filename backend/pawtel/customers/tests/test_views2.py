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


class CustomerViewSetTest2(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.app_user = AppUser.objects.create_user(
            username="customer_user",
            first_name="Jott",
            last_name="otte",
            email="customer@example.com",
            phone="+34987754321",
            password="password123",
        )

        self.customer = Customer.objects.create(user_id=self.app_user.id)
        self.client.force_authenticate(user=self.app_user)

        self.app_user_owner = AppUser.objects.create_user(
            username="hotel_owner",
            first_name="Pepaa",
            last_name="Jimenez",
            email="owner@example.com",
            phone="+34999654322",
            password="passwd123",
        )
        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user_owner.id)

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
            description="Luxury suite",
            capacity=2,
            num_rooms=3,
            price_per_night=150.00,
            pet_type="DOG",
        )

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

    def test_list_bookings_of_customer_explicit(self):
        url = reverse(
            "customer-list_bookings_of_customer_explicit",
            kwargs={"pk": self.customer.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_bookings_of_customer_explicit_unauthorized(self):
        other_user = AppUser.objects.create_user(
            username="other_customer",
            email="other@example.com",
            phone="+34987654323",
            password="password123",
        )
        Customer.objects.create(user=other_user)
        self.client.force_authenticate(user=other_user)
        url = reverse(
            "customer-list_bookings_of_customer_explicit",
            kwargs={"pk": self.customer.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_bookings_of_customer_implicit(self):
        url = reverse("customer-list_bookings_of_customer_implicit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
