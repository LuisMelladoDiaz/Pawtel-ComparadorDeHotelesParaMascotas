from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import PermissionDenied


class HotelOwnerServiceTest(TestCase):

    def setUp(self):
        self.app_user = AppUser.objects.create(
            username="active_owner",
            email="active_owner@example.com",
            phone="+34123456789",
            password="123456",
            is_active=True,
        )
        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user.id)

        self.app_user2 = AppUser.objects.create(
            username="active_user",
            email="active_userr@example.com",
            phone="+34123456719",
            password="123456",
            is_active=True,
        )
        self.customer = Customer.objects.create(user_id=self.app_user2.id)

        self.invalid_user = AppUser.objects.create(
            username="invalid",
            email="invalid@example.com",
            phone="+34123256789",
            password="123456",
            is_active=True,
        )

    def test_get_all_hotels_of_hotel_owner(self):
        hotel1 = Hotel.objects.create(
            name="Hotel One", hotel_owner=self.hotel_owner, is_archived=False
        )
        hotel2 = Hotel.objects.create(
            name="Hotel Two", hotel_owner=self.hotel_owner, is_archived=False
        )
        hotel_archived = Hotel.objects.create(
            name="Hotel Archived", hotel_owner=self.hotel_owner, is_archived=True
        )
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(self.hotel_owner.id)
        self.assertListEqual(list(hotels), [hotel1, hotel2])
        self.assertNotIn(hotel_archived, hotels)

    def test_get_all_hotels_of_hotel_owner_no_hotels(self):
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(self.hotel_owner.id)
        self.assertListEqual(list(hotels), [])

    def test_delete_all_hotels_of_hotel_owner(self):
        Hotel.objects.create(
            name="Hotel A", hotel_owner=self.hotel_owner, is_archived=False
        )
        Hotel.objects.create(
            name="Hotel B", hotel_owner=self.hotel_owner, is_archived=False
        )
        HotelOwnerService.delete_all_hotels_of_hotel_owner(self.hotel_owner.id)
        hotels = Hotel.objects.filter(hotel_owner=self.hotel_owner)
        self.assertEqual(hotels.count(), 0)

    def test_delete_all_hotels_of_hotel_owner_no_hotels(self):
        with self.assertRaises(PermissionDenied, msg="No hotels to delete."):
            HotelOwnerService.delete_all_hotels_of_hotel_owner(self.hotel_owner.id)

    def test_customer_permissions_denied(self):
        action = "list"
        with self.assertRaises(PermissionDenied):
            HotelOwnerService.check_permission(self.app_user2, action)

    def test_hotel_owner_permissions_allowed(self):
        action = "retrieve"
        result, user_type = HotelOwnerService.check_permission(self.app_user, action)
        self.assertTrue(result)
        self.assertEqual(user_type, "HotelOwner")

    def test_hotel_owner_permissions_denied(self):
        action = "some_denied_action_for_owner"
        with self.assertRaises(PermissionDenied):
            HotelOwnerService.check_permission(self.app_user, action)

    def test_invalid_role_permission_denied(self):
        action = "retrieve"
        with self.assertRaises(PermissionDenied):
            HotelOwnerService.check_permission(self.invalid_user, action)
