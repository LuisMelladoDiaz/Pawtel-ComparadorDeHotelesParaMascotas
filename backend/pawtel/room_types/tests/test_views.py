from django.urls import reverse
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class RoomTypeViewSetTests(APITestCase):
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
        self.owner = HotelOwner.objects.create(user_id=self.app_user.id)

        self.hotel = Hotel.objects.create(name="Hotel Pawtel", hotel_owner=self.owner)

        self.room_type_1 = RoomType.objects.create(
            name="Suite",
            description="Luxury suite for pets",
            capacity=10,
            num_rooms=10,
            price_per_night=100.00,
            pet_type="DOG",
            hotel=self.hotel,
            is_archived=False,
        )
        self.room_type_2 = RoomType.objects.create(
            name="Standard",
            description="Standard room for pets",
            capacity=5,
            num_rooms=66,
            price_per_night=50.00,
            pet_type="CAT",
            hotel=self.hotel,
            is_archived=True,
        )

        self.client.force_authenticate(user=self.app_user)

    def test_list_room_types(self):
        url = reverse("room-type-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_room_type(self):
        url = reverse("room-type-detail", args=[self.room_type_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.room_type_1.name)

    def test_create_room_type(self):
        url = reverse("room-type-list")
        data = {
            "name": "Deluxe",
            "description": "Deluxe room description",
            "capacity": 3,
            "num_rooms": 0,
            "price_per_night": "200.00",
            "pet_type": "CAT",
            "hotel": self.hotel.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Deluxe")

    def test_update_room_type(self):
        url = reverse("room-type-detail", args=[self.room_type_1.id])
        data = {
            "name": "Updated Suite",
            "description": "Suite updated room description",
            "capacity": 4,
            "num_rooms": 10,
            "price_per_night": "250.00",
            "pet_type": "CAT",
            "hotel": self.hotel.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Suite")

    def test_partial_update_room_type(self):
        url = reverse("room-type-detail", args=[self.room_type_1.id])
        data = {
            "description": "Updated description",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Updated description")

    def test_destroy_room_type(self):
        url = reverse("room-type-detail", args=[self.room_type_1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
