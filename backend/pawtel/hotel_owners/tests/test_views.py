from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from rest_framework import status
from rest_framework.test import APIClient


class HotelOwnerViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.authenticated_user = AppUser.objects.create_user(
            username="authenticated_user",
            email="authenticated_user@example.com",
            phone="+34111222333",
            password="123456",
            is_active=True,
        )
        self.authenticated_hotel_owner = HotelOwner.objects.create(
            user_id=self.authenticated_user.id
        )
        self.client.force_authenticate(user=self.authenticated_user)

        self.inactive_app_user = AppUser.objects.create(
            username="inactive_owner",
            email="inactive_owner@example.com",
            phone="+34123456788",
            password="123456",
            is_active=False,
        )
        self.inactive_hotel_owner = HotelOwner.objects.create(
            user_id=self.inactive_app_user.id
        )

        self.hotel1 = Hotel.objects.create(
            name="Hotel 1", hotel_owner=self.authenticated_hotel_owner
        )
        self.hotel2 = Hotel.objects.create(
            name="Hotel 2", hotel_owner=self.authenticated_hotel_owner
        )

    def test_get_hotel_owner(self):
        url = reverse(
            "hotel-owner-detail", kwargs={"pk": self.authenticated_hotel_owner.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["user"]["username"],
            self.authenticated_hotel_owner.user.username,
        )

    def test_list_all_hotel_owners(self):
        url = reverse("hotel-owner-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_all_hotels_of_hotel_owner(self):
        url = reverse(
            "hotel-owner-get_all_hotels_of_hotel_owner",
            kwargs={"pk": self.authenticated_hotel_owner.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_all_hotels_of_inactive_hotel_owner(self):
        url = reverse(
            "hotel-owner-get_all_hotels_of_hotel_owner",
            kwargs={"pk": self.inactive_hotel_owner.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_hotels_of_hotel_owner(self):
        url = reverse(
            "hotel-owner-delete_all_hotels_of_hotel_owner",
            kwargs={"pk": self.authenticated_hotel_owner.id},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Hotel.objects.filter(hotel_owner=self.authenticated_hotel_owner).exists()
        )

    def test_delete_all_hotels_of_inactive_hotel_owner(self):
        url = reverse(
            "hotel-owner-delete_all_hotels_of_hotel_owner",
            kwargs={"pk": self.inactive_hotel_owner.id},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_hotel_owner(self):
        url = reverse(
            "hotel-owner-detail", kwargs={"pk": self.authenticated_hotel_owner.id}
        )
        data = {
            "username": "usernameUpdated",
            "email": "updated@example.com",
            "phone": "+34123456780",
            "password": "abcdef",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.authenticated_hotel_owner.refresh_from_db()
        self.assertEqual(self.authenticated_hotel_owner.user.email, data["email"])
        self.assertTrue(
            check_password(
                data["password"], self.authenticated_hotel_owner.user.password
            )
        )

    def test_update_hotel_owner_same_data(self):
        url = reverse(
            "hotel-owner-detail", kwargs={"pk": self.authenticated_hotel_owner.id}
        )
        data = {
            "username": "active_owner_2",
            "email": "active_owner@example.com",
            "phone": "+34123456789",
            "password": "abcdef",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.authenticated_hotel_owner.refresh_from_db()
        self.assertEqual(
            self.authenticated_hotel_owner.user.email, "active_owner@example.com"
        )

    def test_update_hotel_owner_inactive(self):
        url = reverse("hotel-owner-detail", kwargs={"pk": self.inactive_hotel_owner.id})
        data = {
            "username": self.inactive_hotel_owner.user.username,
            "email": "updated@example.com",
            "phone": "+34123456780",
            "password": "abcdef",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_hotel_owner(self):
        url = reverse(
            "hotel-owner-detail", kwargs={"pk": self.authenticated_hotel_owner.id}
        )
        data = {"phone": "+34223344554"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.authenticated_hotel_owner.refresh_from_db()
        self.assertEqual(self.authenticated_hotel_owner.user.phone, "+34223344554")

    def test_partial_update_hotel_owner_inactive(self):
        url = reverse("hotel-owner-detail", kwargs={"pk": self.inactive_hotel_owner.id})
        data = {"phone": "+34223344555"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_hotel_owner(self):
        url = reverse(
            "hotel-owner-detail", kwargs={"pk": self.authenticated_hotel_owner.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            HotelOwner.objects.filter(id=self.authenticated_hotel_owner.id).exists()
        )

    def test_delete_hotel_owner_inactive(self):
        url = reverse("hotel-owner-detail", kwargs={"pk": self.inactive_hotel_owner.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
