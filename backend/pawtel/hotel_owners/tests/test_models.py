from django.core.exceptions import ValidationError
from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner


class HotelOwnerModelTest(TestCase):

    def test_create_valid_hotel_owner(self):
        app_user = AppUser.objects.create_user(
            username="appuser1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        hotel_owner = HotelOwner(user=app_user)

        self.assertEqual(hotel_owner.user.username, "appuser1")
        self.assertEqual(hotel_owner.user.first_name, "John")
        self.assertEqual(hotel_owner.user.last_name, "Doe")
        self.assertEqual(hotel_owner.user.email, "owner@example.com")
        self.assertEqual(hotel_owner.user.phone, "+34987654321")
        self.assertTrue(hotel_owner.user.check_password("securepassword123"))
        self.assertTrue(hotel_owner.user.is_active)
        self.assertFalse(hotel_owner.user.is_staff)
        self.assertFalse(hotel_owner.user.is_superuser)

    def test_create_hotel_without_owner(self):
        hotel_owner = HotelOwner()
        with self.assertRaises(ValidationError):
            hotel_owner.full_clean()

    def test_create_hotel_invalid_owner(self):
        invalid_app_users = ["", 123, {}, []]

        for app_user in invalid_app_users:
            with self.subTest(user=app_user):
                with self.assertRaises(ValueError):
                    HotelOwner.objects.create(user=app_user)
