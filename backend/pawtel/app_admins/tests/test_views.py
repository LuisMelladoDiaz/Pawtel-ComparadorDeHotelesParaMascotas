from django.test import TestCase
from django.urls import reverse
from pawtel.app_admins.models import App_Admin
from pawtel.app_users.models import AppUser
from rest_framework import status
from rest_framework.test import APIClient


class AdminViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = AppUser.objects.create_user(
            username="admin1",
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.admin = App_Admin.objects.create(user=self.admin_user)
        self.client.force_authenticate(user=self.admin_user)

    def test_list_admins(self):
        url = reverse("admin-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data[0])
        self.assertIn("user", response.data[0])

    def test_retrieve_admin(self):
        url = reverse("admin-detail", kwargs={"pk": self.admin.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.admin.id)
        self.assertEqual(response.data["user"]["username"], self.admin_user.username)

    def test_create_admin_not_allowed(self):
        url = reverse("admin-list")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_admin(self):
        url = reverse("admin-detail", kwargs={"pk": self.admin.id})
        data = {
            "username": "UpdatedAdmin",
            "email": "updatedAdmin@example.com",
            "phone": "+34127456789",
            "password": "abcdef",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin.user.username, "UpdatedAdmin")

    def test_partial_update_admin(self):
        url = reverse("admin-detail", kwargs={"pk": self.admin.id})
        data = {"username": "UpdatedLastName"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.username, "UpdatedLastName")

    def test_destroy_admin(self):
        url = reverse("admin-detail", kwargs={"pk": self.admin.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(App_Admin.objects.filter(id=self.admin.id).exists())

    def test_retrieve_current_admin(self):
        url = reverse("admin-retrieve_current_customer")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], self.admin_user.username)
