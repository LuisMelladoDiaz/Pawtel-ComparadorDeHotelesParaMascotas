from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.room_types.services import RoomTypeService
from rest_framework.exceptions import PermissionDenied


class RoomTypeServiceTest(TestCase):
    def setUp(self):
        self.customer_user = AppUser.objects.create_user(
            username="customer1",
            email="customer@example.com",
            password="testpassword123",
            phone="+34987652321",
        )
        self.customer = Customer.objects.create(user_id=self.customer_user.id)

        self.hotel_owner_user = AppUser.objects.create_user(
            username="hotelowner1",
            email="owner@example.com",
            password="testpassword123",
            phone="+34987654321",
        )
        self.hotel_owner = HotelOwner.objects.create(user_id=self.hotel_owner_user.id)

    def test_customer_allowed_actions(self):
        allowed_actions = ["retrieve"]
        for action in allowed_actions:
            result, user_type = RoomTypeService.check_permission(
                self.customer_user, action
            )
            self.assertTrue(result)
            self.assertEqual(user_type, "Customer")

    def test_customer_denied_actions(self):
        denied_actions = ["list", "create", "update", "destroy"]
        for action in denied_actions:
            with self.assertRaises(PermissionDenied):
                RoomTypeService.check_permission(self.customer_user, action)

    def test_hotel_owner_allowed_actions(self):
        allowed_actions = ["list", "retrieve", "create", "update", "destroy"]
        for action in allowed_actions:
            result, user_type = RoomTypeService.check_permission(
                self.hotel_owner_user, action
            )
            self.assertTrue(result)
            self.assertEqual(user_type, "HotelOwner")
