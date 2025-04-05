from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from pawtel.app_admins.models import App_Admin
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from rest_framework import status
from rest_framework.test import APIClient


class HotelOwnerViewSetTest(TestCase):
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
        response = self.client2.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_hotels_of_hotel_owner_explicit(self):
        url = reverse(
            "hotel-owner-list_hotels_of_hotel_owner_explicit",
            kwargs={"pk": self.authenticated_hotel_owner.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_all_hotels_of_inactive_hotel_owner_explicit(self):
        url = reverse(
            "hotel-owner-list_hotels_of_hotel_owner_explicit",
            kwargs={"pk": self.inactive_hotel_owner.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_hotels_of_hotel_owner_implicit(self):
        url = reverse("hotel-owner-list_hotels_of_hotel_owner_implicit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_all_hotels_of_hotel_owner_explicit(self):
        url = reverse(
            "hotel-owner-delete_all_hotels_of_hotel_owner_explicit",
            kwargs={"pk": self.authenticated_hotel_owner.id},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Hotel.objects.filter(hotel_owner=self.authenticated_hotel_owner).exists()
        )

    def test_delete_all_hotels_of_inactive_hotel_owner_explicit(self):
        url = reverse(
            "hotel-owner-delete_all_hotels_of_hotel_owner_explicit",
            kwargs={"pk": self.inactive_hotel_owner.id},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_hotels_of_hotel_owner_implicit(self):
        url = reverse("hotel-owner-delete_all_hotels_of_hotel_owner_implicit")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Hotel.objects.filter(hotel_owner=self.authenticated_hotel_owner).exists()
        )

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

    def test_approve_hotel_owner_patch_view(self):
        url = reverse(
            "hotel-owner-approve_hotel_owner_patch",
            kwargs={"pk": self.authenticated_hotel_owner.id},
        )
        response = self.client2.patch(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_approved"], True)

    def test_delete_unapproved_hotel_owner_view_as_admin(self):
        unapproved_user = AppUser.objects.create_user(
            username="to_delete_view",
            email="delete_view@example.com",
            phone="+34666555444",
            password="123456",
        )
        hotel_owner = HotelOwner.objects.create(user=unapproved_user, is_approved=False)

        url = reverse(
            "hotel-owner-delete_unapproved_hotel_owner",
            kwargs={"pk": hotel_owner.id},
        )
        response = self.client2.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AppUser.objects.filter(id=unapproved_user.id).exists())
        self.assertFalse(HotelOwner.objects.filter(id=hotel_owner.id).exists())

    def test_delete_hotel_owner_as_admin(self):
        url = reverse(
            "hotel-owner-detail", kwargs={"pk": self.authenticated_hotel_owner.id}
        )
        response = self.client2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            HotelOwner.objects.filter(id=self.authenticated_hotel_owner.id).exists()
        )

    def test_list_unapproved_hotel_owners_view_as_admin(self):

        h1 = HotelOwner.objects.create(
            user=AppUser.objects.create_user(
                username="unap1",
                email="u1@example.com",
                phone="+34000111222",
                password="123456",
            ),
            is_approved=False,
        )
        h2 = HotelOwner.objects.create(
            user=AppUser.objects.create_user(
                username="unap2",
                email="u2@example.com",
                phone="+34000111223",
                password="123456",
            ),
            is_approved=False,
        )
        approved = HotelOwner.objects.create(
            user=AppUser.objects.create_user(
                username="appr",
                email="a@example.com",
                phone="+34000111224",
                password="123456",
            ),
            is_approved=True,
        )

        url = reverse("hotel-owner-list_unapproved_hotel_owners")
        response = self.client2.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(not ho["is_approved"] for ho in response.data))

        response_ids = {ho["id"] for ho in response.data}
        expected_ids = {h1.id, h2.id}
        self.assertTrue(expected_ids.issubset(response_ids))
