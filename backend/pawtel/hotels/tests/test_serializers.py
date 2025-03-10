from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer


class HotelSerializerTest(TestCase):

    def setUp(self):
        self.app_user = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user.id)
        self.valid_data = {
            "name": "Hotel Paradise",
            "address": "123 Sunshine Street",
            "city": "Miami",
            "description": "Un hotel lujoso en Miami.",
            "hotel_owner": self.hotel_owner.id,
        }
        self.invalid_data = self.valid_data.copy()
        self.invalid_data["name"] = ""

    # POST tests -------------------------------------------------------------

    def test_serializer_valid_data_post(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = HotelSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], self.valid_data["name"])

    def test_serializer_missing_required_field_post(self):
        # 'description' field deleted
        invalid_data = self.valid_data.copy()
        invalid_data.pop("description")
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = HotelSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_invalid_name_length_post(self):
        invalid_data = self.valid_data.copy()
        invalid_data["name"] = "a" * 101
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = HotelSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_missing_hotel_owner_post(self):
        # 'HotelOwner' field deleted
        invalid_data = self.valid_data.copy()
        invalid_data.pop("hotel_owner")
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = HotelSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("hotel_owner", serializer.errors)

    def test_ignore_additional_fields_for_post(self):
        data = self.valid_data.copy()
        data["is_archived"] = True
        data["extra_field"] = "valor extra"
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = HotelSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("extra_field", serializer.validated_data)

    # PUT tests --------------------------------------------------------------

    def test_serializer_valid_data_put(self):
        context = {"request": type("Request", (), {"method": "PUT"})}
        serializer = HotelSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_ignore_additional_fields_for_put(self):
        data = self.valid_data.copy()
        data["is_archived"] = True
        data["hotel_owner"] = None
        data["extra_field"] = "valor extra"
        context = {"request": type("Request", (), {"method": "PUT"})}
        serializer = HotelSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("hotel_owner", serializer.validated_data)
        self.assertNotIn("extra_field", serializer.validated_data)

    # PATCH tests ------------------------------------------------------------

    def test_serializer_valid_data_patch(self):
        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = HotelSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_ignore_additional_fields_for_patch(self):
        data = {
            "name": "Hotel Paradise Updated",
            "extra_field": "valor extra",
            "is_archived": True,
        }
        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = HotelSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], data["name"])
        self.assertNotIn("extra_field", serializer.validated_data)
        self.assertNotIn("is_archived", serializer.validated_data)

    # GET tests --------------------------------------------------------------

    def test_serializer_get_method(self):
        hotel = Hotel.objects.create(
            name=self.valid_data["name"],
            address=self.valid_data["address"],
            city=self.valid_data["city"],
            description=self.valid_data["description"],
            hotel_owner=self.hotel_owner,
        )
        context = {"request": type("Request", (), {"method": "GET"})}
        serializer = HotelSerializer(hotel, context=context)
        self.assertEqual(serializer.data["name"], hotel.name)
        self.assertEqual(serializer.data["address"], hotel.address)
        self.assertEqual(serializer.data["city"], hotel.city)
        self.assertEqual(serializer.data["description"], hotel.description)
        # read_only fields must be in the response
        self.assertIn("is_archived", serializer.data)
        self.assertIn("id", serializer.data)

    # Other tests ---------------------------------------

    def test_create_hotel_instance_from_json(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = HotelSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        hotel = serializer.create(serializer.validated_data)
        self.assertEqual(hotel.name, self.valid_data["name"])
        self.assertEqual(hotel.city, self.valid_data["city"])
        self.assertEqual(hotel.hotel_owner.id, self.valid_data["hotel_owner"])

    def test_save_hotel_instance_from_json(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = HotelSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        hotel = serializer.save()
        self.assertEqual(hotel.name, self.valid_data["name"])
        self.assertEqual(hotel.city, self.valid_data["city"])
        self.assertEqual(hotel.hotel_owner.id, self.valid_data["hotel_owner"])

    def test_serialize_hotel_instance_to_json(self):
        hotel = Hotel.objects.create(
            name=self.valid_data["name"],
            address=self.valid_data["address"],
            city=self.valid_data["city"],
            description=self.valid_data["description"],
            hotel_owner=self.hotel_owner,
        )
        serializer = HotelSerializer(hotel)
        self.assertEqual(serializer.data["name"], hotel.name)
        self.assertEqual(serializer.data["address"], hotel.address)
        self.assertEqual(serializer.data["city"], hotel.city)
        self.assertEqual(serializer.data["description"], hotel.description)
        self.assertEqual(serializer.data["hotel_owner"], hotel.hotel_owner.id)
