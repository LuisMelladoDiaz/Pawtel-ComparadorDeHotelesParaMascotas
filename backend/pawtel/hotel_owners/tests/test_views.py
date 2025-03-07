from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from rest_framework import status
from rest_framework.test import APIClient


class HotelOwnerViewSetTest(TestCase):
    def setUp(self):
        """Set up a test user and client"""
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

    def test_create_hotel_owner(self):
        """Test creating a new hotel owner"""
        url = reverse("hotel-owner-list")
        data = {
            "username": "newowner",
            "email": "newowner@example.com",
            "phone": "+34123456781",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HotelOwner.objects.filter(username="newowner").exists())

    def test_get_hotel_owner(self):
        """Test retrieving a specific hotel owner"""
        url = reverse("hotel-owner-detail", kwargs={"pk": self.active_hotel_owner.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.active_hotel_owner.email)

    def test_list_all_hotel_owners(self):
        """Test retrieving the list of all hotel owners"""
        url = reverse("hotel-owner-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_all_hotels_of_hotel_owner(self):
        """Test retrieving all hotels of a hotel owner"""
        url = reverse(
            "hotel-owner-get-all-hotels-of-hotel-owner",
            kwargs={"pk": self.active_hotel_owner.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_all_hotels_of_hotel_owner(self):
        """Test deleting all hotels of a hotel owner"""
        url = reverse(
            "hotel-owner-delete-all-hotels-of-hotel-owner",
            kwargs={"pk": self.active_hotel_owner.id},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Hotel.objects.filter(hotel_owner=self.active_hotel_owner).exists()
        )

    def test_update_hotel_owner(self):
        """Test updating a hotel owner"""
        url = reverse("hotel-owner-detail", kwargs={"pk": self.active_hotel_owner.id})
        data = {
            "username": self.active_hotel_owner.username,
            "email": "updated@example.com",
            "phone": "+34123456780",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.active_hotel_owner.refresh_from_db()
        self.assertEqual(self.active_hotel_owner.email, "updated@example.com")

    def test_update_hotel_owner_inactive(self):
        """Test updating a hotel owner, but the hotel owner is inactive"""
        url = reverse("hotel-owner-detail", kwargs={"pk": self.inactive_hotel_owner.id})
        data = {
            "username": self.inactive_hotel_owner.username,
            "email": "updated@example.com",
            "phone": "+34123456780",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_hotel_owner(self):
        """Test partially updating a hotel owner"""
        url = reverse("hotel-owner-detail", kwargs={"pk": self.active_hotel_owner.id})
        data = {"phone": "+34223344554"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.active_hotel_owner.refresh_from_db()
        self.assertEqual(self.active_hotel_owner.phone, "+34223344554")

    def test_partial_update_hotel_owner_inactive(self):
        """Test partially updating a hotel owner, but the hotel owner is inactive"""
        url = reverse("hotel-owner-detail", kwargs={"pk": self.inactive_hotel_owner.id})
        data = {"phone": "+34223344555"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hotel_owner(self):
        """Test deleting a hotel owner"""
        url = reverse("hotel-owner-detail", kwargs={"pk": self.active_hotel_owner.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            HotelOwner.objects.filter(id=self.active_hotel_owner.id).exists()
        )

    def test_delete_hotel_owner_inactive(self):
        """Test deleting a hotel owner, but the hotel owner is inactive"""
        url = reverse("hotel-owner-detail", kwargs={"pk": self.inactive_hotel_owner.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
