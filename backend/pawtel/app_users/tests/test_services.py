from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.app_users.services import AppUserService


class AppUserServiceTest(TestCase):

    def test_general_create_hotel_owner(self):
        data = {
            "username": "newowner",
            "email": "newowner@example.com",
            "phone": "+34123456781",
            "password": "abcdef",
            "is_active": True,
        }
        request = type("Request", (), {"data": data, "method": "POST"})
        response = AppUserService.general_create_app_user(request)
        self.assertEqual(response.username, "newowner")
        self.assertTrue(AppUser.objects.filter(username="newowner").exists())

    def test_general_update_hotel_owner(self):
        self.app_user = AppUser.objects.create(
            username="owner",
            email="owner@example.com",
            phone="+34123456781",
            password="abcdef",
            is_active=True,
        )
        data = {
            "username": "newowner",
            "email": "newowner@example.com",
            "phone": "+34123456781",
            "password": "abcdef",
            "is_active": True,
        }
        request = type("Request", (), {"data": data, "method": "PUT"})
        AppUserService.general_update_app_user(request, self.app_user.id)
        self.assertTrue(AppUser.objects.filter(username="newowner").exists())

    def test_general_delete_hotel_owner(self):
        self.app_user = AppUser.objects.create(
            username="owner",
            email="owner@example.com",
            phone="+34123456781",
            password="abcdef",
            is_active=True,
        )
        request = type("Request", (), {"method": "DELETE"})
        AppUserService.general_delete_app_user(request, self.app_user.id)
        self.assertFalse(AppUser.objects.filter(username="owner").exists())
