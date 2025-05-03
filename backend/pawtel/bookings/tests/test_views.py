from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from pawtel.app_admins.models import App_Admin
from pawtel.app_users.models import AppUser
from pawtel.booking_holds.models import BookingHold
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
        self.client2 = APIClient()
        self.admin_user = AppUser.objects.create_user(
            username="admin1",
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            phone="+34987654221",
            password="securepassword123",
        )
        self.admin = App_Admin.objects.create(user=self.admin_user)
        self.client2.force_authenticate(user=self.admin_user)

        self.app_user_customer1 = AppUser.objects.create_user(
            username="customer_david",
            first_name="David",
            last_name="Johnson",
            email="david@example.com",
            phone="+34447654321",
            password="david_password",
        )

        self.app_user_customer2 = AppUser.objects.create_user(
            username="customer_elena",
            first_name="Elena",
            last_name="Martínez",
            email="elena@example.com",
            phone="+34447654322",
            password="elena_password",
        )

        self.app_user_hotel_owner = AppUser.objects.create_user(
            username="hotelowner_sanse",
            first_name="Sanse",
            last_name="Smith",
            email="sanse@example.com",
            phone="+34987655555",
            password="hotel_password",
        )

        self.customer1 = Customer.objects.create(user=self.app_user_customer1)
        self.customer2 = Customer.objects.create(user=self.app_user_customer2)
        self.hotel_owner = HotelOwner.objects.create(user=self.app_user_hotel_owner)

        self.hotel1 = Hotel.objects.create(
            name="Hotel de la esperanza",
            address="Calle Deportes",
            city="Barcelona",
            description="Hotel exclusivo con spa y piscina",
            hotel_owner=self.hotel_owner,
        )

        self.hotel2 = Hotel.objects.create(
            name="Hotel Luna Azul",
            address="Avenida del Sol",
            city="Madrid",
            description="Hotel boutique con vista a la playa",
            hotel_owner=self.hotel_owner,
        )

        self.room_type1 = RoomType.objects.create(
            hotel=self.hotel1,
            name="Habitación Premium",
            description="Habitación de lujo con balcón",
            capacity=2,
            num_rooms=2,
            price_per_night=250.00,
            pet_type="DOG",
        )

        self.room_type2 = RoomType.objects.create(
            hotel=self.hotel2,
            name="Suite Familiar",
            description="Suite con capacidad para toda la familia",
            capacity=4,
            num_rooms=2,
            price_per_night=400.00,
            pet_type="CAT",
        )

        self.booking1 = Booking.objects.create(
            customer=self.customer1,
            room_type=self.room_type1,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=750.00,
        )

        self.booking2 = Booking.objects.create(
            customer=self.customer2,
            room_type=self.room_type2,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=6),
            total_price=1200.00,
        )

        self.client.force_authenticate(user=self.app_user_customer1)

    def test_list_bookings(self):
        url = reverse("booking-list")
        response = self.client2.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_booking_valid(self):
        url = reverse("booking-detail", kwargs={"pk": self.booking1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.booking1.id)

    def test_create_booking_hold_when_start_booking(self):
        url = reverse("booking-list")
        data = {
            "start_date": str(date.today() + timedelta(days=30)),
            "end_date": str(date.today() + timedelta(days=37)),
            "room_type": self.room_type2.id,
            "use_paw_points": "false",
        }
        response = self.client.post(url, data, format="json")

        booking_holds_of_customer = BookingHold.objects.filter(
            customer_id=self.customer1.id
        ).all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(booking_holds_of_customer), 1)
