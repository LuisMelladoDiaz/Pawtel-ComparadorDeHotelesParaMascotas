from django.test import RequestFactory, TestCase
from pawtel.app_users.models import AppUser
from pawtel.app_users.serializers import AppUserSerializer


class AppUserSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "id": 1,
            "username": "appuser1",
            "email": "appuser1@example.com",
            "phone": "+34111222333",
            "password": "securepassword123",
            "accept_terms": True,
        }
        self.invalid_data = {
            "id": 1,
            "username": "appuser2",
            "email": "invalid-email",  # Invalid email
            "phone": "123",  # Invalid phone number format
            "password": "short",  # Password too short
            "accept_terms": True,
        }

    # POST tests -------------------------------------------------------------

    def test_serializer_valid_data_post(self):
        factory = RequestFactory()
        # Create a proper POST request with data
        request = factory.post("/fake-url/", data=self.valid_data)

        # The request object needs to have META attributes
        request.META = {}  # Initialize META if not already present
        request.META["REMOTE_ADDR"] = "127.0.0.1"  # Add a fake IP address

        context = {"request": request}
        serializer = AppUserSerializer(data=self.valid_data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["username"], self.valid_data["username"]
        )
        self.assertEqual(
            serializer.validated_data["password"], self.valid_data["password"]
        )

    def test_serializer_invalid_email_post(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"  # Invalid email format
        context = {"request": type("Request", (), {"method": "POST"})}

        serializer = AppUserSerializer(data=invalid_data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_serializer_invalid_phone_post(self):
        invalid_data = self.valid_data.copy()
        invalid_data["phone"] = "123"  # Invalid phone format
        context = {"request": type("Request", (), {"method": "POST"})}

        serializer = AppUserSerializer(data=invalid_data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_required_fields_for_post(self):
        incomplete_data = {
            "id": 1,
            "username": "appuser3",
            "email": "appuser3@example.com",
            # Missing phone
        }
        context = {"request": type("Request", (), {"method": "POST"})}

        serializer = AppUserSerializer(data=incomplete_data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_ignore_additional_fields_for_post(self):
        data = {
            "id": 1,
            "username": "appuser7",
            "email": "appuser7@example.com",
            "phone": "+34987654321",
            "password": "securepassword",
            "date_joined": "2025-03-02T12:00:00Z",  # This should be ignored
            "is_active": True,  # This should be ignored
            "accept_terms": True,
        }
        context = {"request": type("Request", (), {"method": "POST"})}

        serializer = AppUserSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("date_joined", serializer.validated_data)
        self.assertNotIn("is_active", serializer.validated_data)

    # PUT tests --------------------------------------------------------------

    def test_serializer_valid_data_put(self):
        context = {"request": type("Request", (), {"method": "PUT"})}

        serializer = AppUserSerializer(data=self.valid_data, context=context)

        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_email_put(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"
        context = {"request": type("Request", (), {"method": "PUT"})}

        serializer = AppUserSerializer(data=invalid_data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_ignore_additional_fields_for_put(self):
        data = {
            "id": 1,
            "username": "appuser8",
            "email": "appuser8@example.com",
            "phone": "+34987654321",
            "password": "securepassword",
            "date_joined": "2025-03-02T12:00:00Z",  # This should be ignored
            "is_active": True,  # This should be ignored
            "accept_terms": True,
        }
        context = {"request": type("Request", (), {"method": "PUT"})}

        serializer = AppUserSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("date_joined", serializer.validated_data)
        self.assertNotIn("is_active", serializer.validated_data)
        self.assertNotIn("whatever", serializer.validated_data)

    # PATCH tests ------------------------------------------------------------

    def test_serializer_valid_data_patch(self):
        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = AppUserSerializer(data=self.valid_data, context=context)

        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_phone_patch(self):
        invalid_data = self.valid_data.copy()
        invalid_data["phone"] = "123"
        context = {"request": type("Request", (), {"method": "PATCH"})}

        serializer = AppUserSerializer(data=invalid_data, context=context)

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_ignore_additional_fields_for_patch(self):
        data = {
            "id": 1,
            "email": "appuser1@example.com",
            "password": "newpassword",
            "date_joined": "2025-03-02T12:00:00Z",  # This should be ignored
            "is_active": False,  # This should be ignored
            "accept_terms": True,
            "whatever": "ignored...",
        }
        context = {"request": type("Request", (), {"method": "PATCH"})}

        serializer = AppUserSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertIn("email", serializer.validated_data)
        self.assertNotIn("date_joined", serializer.validated_data)
        self.assertNotIn("is_active", serializer.validated_data)
        self.assertNotIn("whatever", serializer.validated_data)

    # GET tests --------------------------------------------------------------

    def test_serializer_get_method_removes_first_name(self):
        # Test GET method where password should not be present in the response
        owner = AppUser.objects.create_user(
            username="appuser4",
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone="+34987654321",
            password="password123",
        )
        context = {"request": type("Request", (), {"method": "GET"})}

        serializer = AppUserSerializer(owner, context=context)

        self.assertNotIn("first_name", serializer.data)
        self.assertNotIn("password", serializer.data)
        self.assertIn("username", serializer.data)

    # Other tests ------------------------------------------------------------

    def test_create_app_user_instance_from_json_2(self):
        factory = RequestFactory()
        request = factory.post("/fake-url/")
        request.META = {"REMOTE_ADDR": "127.0.0.1"}

        context = {"request": request}
        serializer = AppUserSerializer(data=self.valid_data, context=context)

        self.assertTrue(serializer.is_valid())
        owner = serializer.create(serializer.validated_data)
        self.assertEqual(owner.username, self.valid_data["username"])

    def test_save_app_user_instance_from_json(self):
        factory = RequestFactory()
        request = factory.post("/fake-url/")
        request.META = {"REMOTE_ADDR": "127.0.0.1"}

        context = {"request": request}
        serializer = AppUserSerializer(data=self.valid_data, context=context)

        self.assertTrue(serializer.is_valid())
        owner = serializer.save()
        self.assertEqual(owner.username, self.valid_data["username"])

    def test_serialize_app_user_instance_to_json(self):
        owner = AppUser.objects.create_user(
            username="appuser5",
            first_name="John",
            last_name="Smith",
            email="john.smith@example.com",
            phone="+34987654321",
            password="password123",
        )

        serializer = AppUserSerializer(owner)

        self.assertEqual(serializer.data["username"], owner.username)
        self.assertEqual(serializer.data["email"], owner.email)
        self.assertEqual(serializer.data["phone"], owner.phone)
        self.assertNotIn("password", serializer.data)
