from django.core.exceptions import ValidationError
from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer


class CustomerModelTest(TestCase):

    def test_create_valid_customer(self):
        app_user = AppUser.objects.create_user(
            username="appuser1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        customer = Customer(user=app_user)

        self.assertEqual(customer.user.username, "appuser1")
        self.assertEqual(customer.user.first_name, "John")
        self.assertEqual(customer.user.last_name, "Doe")
        self.assertEqual(customer.user.email, "owner@example.com")
        self.assertEqual(customer.user.phone, "+34987654321")
        self.assertTrue(customer.user.check_password("securepassword123"))
        self.assertTrue(customer.user.is_active)
        self.assertFalse(customer.user.is_staff)
        self.assertFalse(customer.user.is_superuser)

    def test_create_hotel_without_owner(self):
        customer = Customer()
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_hotel_invalid_owner(self):
        invalid_app_users = ["", 123, {}, []]

        for app_user in invalid_app_users:
            with self.subTest(user=app_user):
                with self.assertRaises(ValueError):
                    Customer.objects.create(user=app_user)
