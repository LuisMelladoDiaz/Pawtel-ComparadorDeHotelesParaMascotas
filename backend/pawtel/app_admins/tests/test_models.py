from django.test import TestCase
from pawtel.app_admins.models import App_Admin
from pawtel.app_users.models import AppUser


class AdminModelTest(TestCase):

    def test_create_valid_admin(self):
        app_user = AppUser.objects.create_user(
            username="adminuser1",
            first_name="Alice",
            last_name="Smith",
            email="admin@example.com",
            phone="+34987654322",
            password="securepassword123",
        )

        admin = App_Admin(user=app_user)

        self.assertEqual(admin.user.username, "adminuser1")
        self.assertEqual(admin.user.first_name, "Alice")
        self.assertEqual(admin.user.last_name, "Smith")
        self.assertEqual(admin.user.email, "admin@example.com")
        self.assertEqual(admin.user.phone, "+34987654322")
        self.assertTrue(admin.user.check_password("securepassword123"))
        self.assertTrue(admin.user.is_active)
        self.assertTrue(admin.user.role == "ADMIN")
