from django.test import TestCase
from pawtel.app_admins.models import App_Admin
from pawtel.app_admins.serializers import AdminSerializer
from pawtel.app_users.models import AppUser


class AdminSerializerTest(TestCase):

    def setUp(self):
        self.app_user = AppUser.objects.create_user(
            username="admin1",
            first_name="Alice",
            last_name="Smith",
            email="admin@example.com",
            phone="+34987654322",
            password="securepassword123",
            is_staff=True,
        )

        self.valid_data = {"user": self.app_user.id}

    # PUT tests --------------------------------------------------------------

    def test_ignore_all_fields_for_put(self):
        data = {
            "id": 1,
            "username": "admin8",
            "email": "admin8@example.com",
            "phone": "+34987654321",
            "password": "securepassword",
            "date_joined": "2025-03-02T12:00:00Z",
            "is_active": True,
            "user": "invalid...",
        }
        context = {"request": type("Request", (), {"method": "PUT"})}

        serializer = AdminSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("user", serializer.validated_data)
        self.assertNotIn("date_joined", serializer.validated_data)
        self.assertNotIn("is_active", serializer.validated_data)

    # PATCH tests ------------------------------------------------------------

    def test_ignore_all_fields_for_patch(self):
        data = {
            "id": 1,
            "username": "admin8",
            "email": "admin8@example.com",
            "phone": "+34987654321",
            "password": "securepassword",
            "date_joined": "2025-03-02T12:00:00Z",
            "is_active": True,
            "user": "invalid...",
        }
        context = {"request": type("Request", (), {"method": "PATCH"})}

        serializer = AdminSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("user", serializer.validated_data)
        self.assertNotIn("date_joined", serializer.validated_data)
        self.assertNotIn("is_active", serializer.validated_data)

    # GET tests --------------------------------------------------------------

    def test_serializer_get_method_removes_sensitive_fields(self):
        # Test GET method where password should not be present in the response
        admin = App_Admin(user=self.app_user)
        context = {"request": type("Request", (), {"method": "GET"})}

        serializer = AdminSerializer(admin, context=context)

        self.assertNotIn("password", serializer.data)
        self.assertIn("user", serializer.data)
        self.assertEqual(serializer.data["user"]["username"], self.app_user.username)

    # Other tests ------------------------------------------------------------

    def test_serialize_admin_instance_to_json(self):
        admin = App_Admin(user=self.app_user)

        serializer = AdminSerializer(admin)

        self.assertEqual(serializer.data["user"]["username"], admin.user.username)
