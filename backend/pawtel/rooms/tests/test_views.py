from django.urls import reverse
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class RoomViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = HotelOwner.objects.create(username="testuser")
        self.owner.set_password("testpass")
        self.owner.save()

        self.hotel = Hotel.objects.create(name="Hotel Pawtel", hotel_owner=self.owner)

        self.room_type = RoomType.objects.create(
            name="Suite",
            description="Luxury suite for pets",
            capacity=10,
            price_per_night=100.00,
            pet_type="DOG",
            hotel=self.hotel,
        )

        self.room1 = Room.objects.create(
            room_type=self.room_type, name="Room 1", is_archived=False
        )

        self.client.force_authenticate(user=self.owner)

    def test_list_rooms(self):
        url = reverse("room-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_room(self):
        url = reverse("room-detail", args=[self.room1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.room1.name)

    def test_create_room(self):
        url = reverse("room-list")
        data = {"room_type": self.room_type.id, "name": "New Room"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Room")

    def test_update_room(self):
        url = reverse("room-detail", args=[self.room1.id])
        data = {
            "name": "Updated Room",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Room")

    def test_partial_update_room(self):
        url = reverse("room-detail", args=[self.room1.id])
        data = {"name": "Partially Updated Room"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Partially Updated Room")

    def test_destroy_room(self):
        url = reverse("room-detail", args=[self.room1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
