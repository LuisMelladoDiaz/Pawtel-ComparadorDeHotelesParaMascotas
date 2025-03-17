from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.customers.services import CustomerService
from pawtel.hotel_owners.models import HotelOwner
from rest_framework.exceptions import PermissionDenied


class CustomerServiceTest(TestCase):

    def setUp(self):
        self.app_user_customer = AppUser.objects.create(
            username="customer_user",
            email="customer@example.com",
            phone="+34123456789",
            password="123456",
            is_active=True,
        )
        self.customer = Customer.objects.create(user_id=self.app_user_customer.id)

        self.app_user_hotelowner = AppUser.objects.create(
            username="hotel_owner",
            email="hotel_owner@example.com",
            phone="+34987654321",
            password="123456",
            is_active=True,
        )
        self.hotel_owner = HotelOwner.objects.create(
            user_id=self.app_user_hotelowner.id
        )

    def test_customer_permissions(self):
        allowed_actions = [
            "list",
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "retrieve_current_customer",
        ]
        denied_actions = ["create"]

        for action in allowed_actions:
            self.assertTrue(
                CustomerService.check_permission(self.app_user_customer, action)
            )

        for action in denied_actions:
            with self.assertRaises(PermissionDenied):
                CustomerService.check_permission(self.app_user_customer, action)

    def test_hotel_owner_permissions(self):
        denied_actions = [
            "create",
            "update",
            "partial_update",
            "destroy",
            "retrieve_current_customer",
            "list",
            "retrieve",
        ]

        for action in denied_actions:
            with self.assertRaises(PermissionDenied):
                CustomerService.check_permission(self.app_user_hotelowner, action)
