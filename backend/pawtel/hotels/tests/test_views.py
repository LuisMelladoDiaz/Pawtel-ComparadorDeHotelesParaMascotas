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

        self.hotel_owner = HotelOwner.objects.create(
            username="hotel_owner",
            email="owner@example.com",
            phone="+34123456789",
            is_active=True,
        )

        self.hotel = Hotel.objects.create(
            name="Test Hotel", hotel_owner=self.hotel_owner
        )

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
        data = {"name": "Updated Hotel"}
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

    def test_get_total_vacancy_for_each_room_type_of_hotel(self):
        url = reverse(
            "hotel-get_total_vacancy_for_each_room_type_of_hotel",
            kwargs={"pk": self.hotel.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
