from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.customers.serializers import CustomerSerializer


class CustomerSerializerTest(TestCase):

    def setUp(self):
        self.app_user = AppUser.objects.create_user(
            username="appuser1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        self.valid_data = {"user": self.app_user.id}

    # POST tests --------------------------------------------------------------

    def test_valid_post(self):
        data = {"paw_points": 99}
        context = {"request": type("Request", (), {"method": "POST"})}

        serializer = CustomerSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertIn("paw_points", serializer.validated_data)

    # PUT tests --------------------------------------------------------------

    def test_ignore_all_fields_for_put(self):
        data = {
            "id": 1,
            "username": "customer8",
            "email": "customer8@example.com",
            "phone": "+34987654321",
            "password": "securepassword",
            "date_joined": "2025-03-02T12:00:00Z",
            "is_active": True,
            "user": "invalid...",
            "paw_points": 0,
        }
        context = {"request": type("Request", (), {"method": "PUT"})}

        serializer = CustomerSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("user", serializer.validated_data)
        self.assertNotIn("date_joined", serializer.validated_data)
        self.assertNotIn("is_active", serializer.validated_data)
        self.assertIn("paw_points", serializer.validated_data)

    # PATCH tests ------------------------------------------------------------

    def test_ignore_all_fields_for_patch(self):
        data = {
            "id": 1,
            "username": "customer8",
            "email": "customer8@example.com",
            "phone": "+34987654321",
            "password": "securepassword",
            "date_joined": "2025-03-02T12:00:00Z",
            "is_active": True,
            "user": "invalid...",
            "paw_points": 0,
        }
        context = {"request": type("Request", (), {"method": "PATCH"})}

        serializer = CustomerSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("user", serializer.validated_data)
        self.assertNotIn("date_joined", serializer.validated_data)
        self.assertNotIn("is_active", serializer.validated_data)
        self.assertIn("paw_points", serializer.validated_data)

    # GET tests --------------------------------------------------------------

    def test_serializer_get_method_removes_first_name(self):
        # Test GET method where password should not be present in the response
        customer = Customer(user=self.app_user)
        context = {"request": type("Request", (), {"method": "GET"})}

        serializer = CustomerSerializer(customer, context=context)

        self.assertNotIn("password", serializer.data)
        self.assertIn("user", serializer.data)
        self.assertEqual(serializer.data["user"]["username"], self.app_user.username)

    # Other tests ------------------------------------------------------------

    def test_serialize_customer_instance_to_json(self):
        customer = Customer(user=self.app_user)

        serializer = CustomerSerializer(customer)

        self.assertEqual(serializer.data["user"]["username"], customer.user.username)
        self.assertEqual(serializer.data.get("paw_points"), 0)
