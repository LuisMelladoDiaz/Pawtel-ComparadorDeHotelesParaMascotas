from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.bookings.models import Booking
from rest_framework import status
from rest_framework.test import APIClient


class HotelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app_user = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.client.force_authenticate(user=self.app_user)

        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user.id)
        self.hotel = Hotel.objects.create(
            name="Test Hotel", hotel_owner=self.hotel_owner
        )
        
        self.app_user_owner2 = AppUser.objects.create_user(
            username="hotelowner2",
            first_name="Alice",
            last_name="Smith",
            email="owner2@example.com",
            phone="+34987654322",
            password="securepassword123",
        )

        self.hotel_owner2 = HotelOwner.objects.create(user_id=self.app_user_owner2.id)

        self.hotel2 = Hotel.objects.create(
            name="Hotel Luna Azul",
            is_archived=False,
            hotel_owner=self.hotel_owner2,
        )

        self.room_type3 = RoomType.objects.create(
            name="Suite",
            hotel=self.hotel2,
            description="Luxury suite",
            capacity=2,
            price_per_night=200.0,
            pet_type="CAT",
        )

        self.booking1 = Booking.objects.create(
            customer=self.hotel_owner,
            room_type=self.room_type1,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=7),
            total_price=400.00,
        )

        self.booking2 = Booking.objects.create(
            customer=self.hotel_owner2,
            room_type=self.room_type3,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=10),
            total_price=1000.00,
        )

    def test_get_all_bookings_by_hotel_explicit(self):
        url = reverse("get_all_bookings_by_hotel_explicit", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.booking1.id)

    def test_get_all_bookings_by_hotel_implicit(self):
        url = reverse("get_all_bookings_by_hotel_implicit")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.booking1.id)

    def test_list_hotels(self):
        url = reverse("hotel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.hotel.name)

    def test_create_hotel(self):
        url = reverse("hotel-list")
        data = {
            "name": "New Hotel",
            "address": "123 Street",
            "city": "Test City",
            "description": "A nice hotel",
            "hotel_owner": self.hotel_owner.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Hotel.objects.filter(name="New Hotel").exists())

    def test_update_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        data = {
            "name": "Updated Hotel",
            "address": "123 Street",
            "city": "Test City",
            "description": "A nice hotel",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, "Updated Hotel")

    def test_partial_update_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        data = {"name": "Partially Updated Hotel"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, "Partially Updated Hotel")

    def test_delete_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hotel.objects.filter(id=self.hotel.id).exists())

    def test_get_all_room_types_of_hotel(self):
        url = reverse("hotel-get_all_room_types_of_hotel", kwargs={"pk": self.hotel.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
