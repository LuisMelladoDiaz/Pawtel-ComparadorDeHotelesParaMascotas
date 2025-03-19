from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from rest_framework import status
from rest_framework.test import APIClient


class CustomerViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.authenticated_user = AppUser.objects.create_user(
            username="authenticated_user",
            email="authenticated_user@example.com",
            phone="+34111222333",
            password="123456",
            is_active=True,
        )
        self.authenticated_customer = Customer.objects.create(
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
        self.inactive_customer = Customer.objects.create(
            user_id=self.inactive_app_user.id
        )

    def test_get_customer(self):
        url = reverse("customer-detail", kwargs={"pk": self.authenticated_customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["user"]["username"],
            self.authenticated_customer.user.username,
        )

    def test_list_all_customers(self):
        url = reverse("customer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_customer(self):
        url = reverse("customer-detail", kwargs={"pk": self.authenticated_customer.id})
        data = {
            "username": "usernameUpdated",
            "email": "updated@example.com",
            "phone": "+34123456780",
            "password": "abcdef",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.authenticated_customer.refresh_from_db()
        self.assertEqual(self.authenticated_customer.user.email, data["email"])
        self.assertTrue(
            check_password(data["password"], self.authenticated_customer.user.password)
        )

    def test_update_customer_same_data(self):
        url = reverse("customer-detail", kwargs={"pk": self.authenticated_customer.id})
        data = {
            "username": "active_owner_2",
            "email": "active_owner@example.com",
            "phone": "+34123456789",
            "password": "abcdef",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.authenticated_customer.refresh_from_db()
        self.assertEqual(
            self.authenticated_customer.user.email, "active_owner@example.com"
        )

    def test_update_customer_inactive(self):
        url = reverse("customer-detail", kwargs={"pk": self.inactive_customer.id})
        data = {
            "username": self.inactive_customer.user.username,
            "email": "updated@example.com",
            "phone": "+34123456780",
            "password": "abcdef",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_customer(self):
        url = reverse("customer-detail", kwargs={"pk": self.authenticated_customer.id})
        data = {"phone": "+34223344554"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.authenticated_customer.refresh_from_db()
        self.assertEqual(self.authenticated_customer.user.phone, "+34223344554")

    def test_partial_update_customer_inactive(self):
        url = reverse("customer-detail", kwargs={"pk": self.inactive_customer.id})
        data = {"phone": "+34223344555"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_customer(self):
        url = reverse("customer-detail", kwargs={"pk": self.authenticated_customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Customer.objects.filter(id=self.authenticated_customer.id).exists()
        )

    def test_delete_customer_inactive(self):
        url = reverse("customer-detail", kwargs={"pk": self.inactive_customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
