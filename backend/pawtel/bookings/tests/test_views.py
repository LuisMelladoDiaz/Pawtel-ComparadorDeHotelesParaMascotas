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


class BookingViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.app_user_customer = AppUser.objects.create_user(
            username="customer30",
            first_name="David",
            last_name="Johnson",
            email="david@example.com",
            phone="+34447654321",
            password="liverpool",
        )
        self.app_user_hotel_owner = AppUser.objects.create_user(
            username="hotelowner30",
            first_name="Sanse",
            last_name="Smith",
            email="sanse@example.com",
            phone="+34987655555",
            password="caberra",
        )

        self.customer = Customer.objects.create(user=self.app_user_customer)
        self.hotel_owner = HotelOwner.objects.create(user=self.app_user_hotel_owner)

        self.hotel = Hotel.objects.create(
            name="Hotel de la esperanza",
            address="Calle deportes",
            city="Barcelona",
            description="Hotel muy refinado para gente con mucha pasta",
            hotel_owner=self.hotel_owner,
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Habitacion premium",
            description="Habitación con mucho caché.",
            capacity=2,
            price_per_night=200.00,
            pet_type="DOG",
        )

        self.booking = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=600.00,
        )

        # Autenticar al cliente
        self.client.force_authenticate(user=self.app_user_customer)

    # GET Method Tests --------------------------------------------------

    def test_list_bookings(self):
        url = reverse("booking-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_booking_valid(self):
        url = reverse("booking-detail", kwargs={"pk": self.booking.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.booking.id)

    def test_retrieve_booking_unauthorized(self):
        # Un Customer no puede ver reservas de otros Customers
        # Crear otro usuario cliente
        app_user_customer2 = AppUser.objects.create_user(
            username="customer2",
            email="customer2@example.com",
            password="securepassword123",
        )
        self.client.force_authenticate(user=app_user_customer2)

        url = reverse("booking-detail", kwargs={"pk": self.booking.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST Method Test --------------------------------------------------

    def test_create_booking(self):
        url = reverse("booking-list")
        data = {
            "room_type": self.room_type.id,
            "start_date": str(date.today() + timedelta(days=3)),
            "end_date": str(date.today() + timedelta(days=6)),
            "total_price": 600.00,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(customer=self.customer).exists())
