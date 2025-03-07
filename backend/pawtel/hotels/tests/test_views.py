from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from rest_framework import status
from rest_framework.test import APIClient


class HotelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.active_hotel_owner = HotelOwner.objects.create(
            username="active_owner",
            email="active_owner@example.com",
            phone="+34123456789",
            is_active=True,
        )
        self.inactive_hotel_owner = HotelOwner.objects.create(
            username="inactive_owner",
            email="inactive_owner@example.com",
            phone="+34123456788",
            is_active=False,
        )

        self.hotel1 = Hotel.objects.create(
            name="Hotel 1", hotel_owner=self.active_hotel_owner
        )
        self.hotel2 = Hotel.objects.create(
            name="Hotel 2", hotel_owner=self.active_hotel_owner
        )

    def test_create_hotel(self):
        url = reverse("hotel-list")
        data = {
            "name": "New Hotel",
            "address": "123 Hotel St.",
            "city": "Test City",
            "description": "A wonderful new hotel.",
            "hotel_owner": self.active_hotel_owner.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Hotel.objects.filter(name="New Hotel").exists())

    def test_get_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.hotel1.name)

    def test_list_all_hotels(self):
        url = reverse("hotel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_all_room_types_of_hotel(self):
        url = reverse(
            "get_all_room_types_of_hotel", kwargs={"pk": self.hotel1.id}
        )  # Corregir el nombre de la URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_total_vacancy_for_each_room_type_of_hotel(self):
        url = reverse(
            "get_total_vacancy_for_each_room_type_of_hotel",
            kwargs={"pk": self.hotel1.id},
        )  # Corregir el nombre de la URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel1.id})

        data = {
            "name": "Updated Hotel Name",
            "address": "123 Main Street",
            "city": "Madrid",
            "description": "A newly renovated hotel in the heart of the city",
            "hotel_owner": self.hotel1.hotel_owner.id,
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel1.refresh_from_db()
        self.assertEqual(self.hotel1.name, "Updated Hotel Name")

    def test_update_archived_hotel(self):
        archived_hotel = Hotel.objects.create(
            name="Archived Hotel", hotel_owner=self.active_hotel_owner, is_archived=True
        )
        url = reverse("hotel-detail", kwargs={"pk": archived_hotel.id})
        data = {"name": "Updated Archived Hotel"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hotel(self):
        url = reverse("hotel-detail", kwargs={"pk": self.hotel1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hotel.objects.filter(id=self.hotel1.id).exists())

    def test_delete_archived_hotel(self):
        archived_hotel = Hotel.objects.create(
            name="Archived Hotel", hotel_owner=self.active_hotel_owner, is_archived=True
        )
        url = reverse("hotel-detail", kwargs={"pk": archived_hotel.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
