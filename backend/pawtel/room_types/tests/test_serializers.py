from decimal import Decimal

from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType
from pawtel.room_types.serializers import RoomTypeSerializer


class RoomTypeSerializerTest(TestCase):

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
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="123 Test St",
            city="Test City",
            description="Descripción del hotel de prueba",
            hotel_owner=self.hotel_owner,
        )
        self.valid_data = {
            "name": "Suite Deluxe",
            "description": "Una habitación de lujo.",
            "capacity": 2,
            "num_rooms": 10,
            "price_per_night": Decimal("150.00"),
            "pet_type": PetType.DOG,  # Could be "DOG", "CAT", "BIRD" o "MIXED"
            "hotel": self.hotel.id,
        }

    # POST tests -------------------------------------------------------------

    def test_serializer_valid_data_post(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], self.valid_data["name"])

    def test_serializer_missing_required_field_post(self):
        # 'description' field deleted
        invalid_data = self.valid_data.copy()
        invalid_data.pop("description")
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_invalid_name_length_post(self):
        invalid_data = self.valid_data.copy()
        invalid_data["name"] = "a" * 51
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_capacity_post(self):
        # Capacity must be equal or greater than 1
        invalid_data = self.valid_data.copy()
        invalid_data["capacity"] = 0
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("capacity", serializer.errors)

    def test_invalid_price_per_night_post(self):
        # price_per_night must be equal or greater than 1.00
        invalid_data = self.valid_data.copy()
        invalid_data["price_per_night"] = Decimal("0.00")
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price_per_night", serializer.errors)

    def test_invalid_pet_type_post(self):
        invalid_data = self.valid_data.copy()
        invalid_data["pet_type"] = "FISH"  # Invalid value
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("pet_type", serializer.errors)

    def test_ignore_additional_fields_for_post(self):
        data = self.valid_data.copy()
        data["is_archived"] = True
        data["extra_field"] = "valor extra"
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("extra_field", serializer.validated_data)

    # PUT tests --------------------------------------------------------------

    def test_serializer_valid_data_put(self):
        context = {"request": type("Request", (), {"method": "PUT"})}
        serializer = RoomTypeSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_ignore_additional_fields_for_put(self):
        data = self.valid_data.copy()
        data["is_archived"] = True
        data["pet_type"] = PetType.CAT  # Not editable in PUT
        data["hotel"] = None  # Not editable in PUT
        data["extra_field"] = "valor extra"
        context = {"request": type("Request", (), {"method": "PUT"})}
        serializer = RoomTypeSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("pet_type", serializer.validated_data)
        self.assertNotIn("hotel", serializer.validated_data)
        self.assertNotIn("extra_field", serializer.validated_data)

    # PATCH tests ------------------------------------------------------------

    def test_serializer_valid_data_patch(self):
        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = RoomTypeSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_ignore_additional_fields_for_patch(self):
        data = {
            "name": "Suite Deluxe Updated",
            "extra_field": "valor extra",
            "is_archived": True,
            "pet_type": PetType.BIRD,  # Not editable
            "hotel": self.hotel.id,  # Not editable
        }
        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = RoomTypeSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], data["name"])
        self.assertNotIn("extra_field", serializer.validated_data)
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("pet_type", serializer.validated_data)
        self.assertNotIn("hotel", serializer.validated_data)

    # GET tests --------------------------------------------------------------

    def test_serializer_get_method(self):
        room_type = RoomType.objects.create(
            name=self.valid_data["name"],
            description=self.valid_data["description"],
            capacity=self.valid_data["capacity"],
            price_per_night=self.valid_data["price_per_night"],
            pet_type=self.valid_data["pet_type"],
            hotel=self.hotel,
        )
        context = {"request": type("Request", (), {"method": "GET"})}
        serializer = RoomTypeSerializer(room_type, context=context)
        self.assertEqual(serializer.data["name"], room_type.name)
        self.assertEqual(serializer.data["description"], room_type.description)
        self.assertEqual(serializer.data["capacity"], room_type.capacity)
        self.assertEqual(
            str(serializer.data["price_per_night"]), str(room_type.price_per_night)
        )
        self.assertEqual(serializer.data["pet_type"], room_type.pet_type)
        self.assertEqual(serializer.data["hotel"], room_type.hotel.id)
        self.assertIn("id", serializer.data)
        self.assertIn("is_archived", serializer.data)

    # Other tests ---------------------------------------

    def test_create_room_type_instance_from_json(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # The instance is created but not saved in the database
        room_type = serializer.create(serializer.validated_data)
        self.assertEqual(room_type.name, self.valid_data["name"])
        self.assertEqual(room_type.hotel.id, self.valid_data["hotel"])

    def test_save_room_type_instance_from_json(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomTypeSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # The instance is created and saved in the database
        room_type = serializer.save()
        self.assertEqual(room_type.name, self.valid_data["name"])
        self.assertEqual(room_type.hotel.id, self.valid_data["hotel"])

    def test_serialize_room_type_instance_to_json(self):
        room_type = RoomType.objects.create(
            name=self.valid_data["name"],
            description=self.valid_data["description"],
            capacity=self.valid_data["capacity"],
            price_per_night=self.valid_data["price_per_night"],
            pet_type=self.valid_data["pet_type"],
            hotel=self.hotel,
        )
        serializer = RoomTypeSerializer(room_type)
        self.assertEqual(serializer.data["name"], room_type.name)
        self.assertEqual(serializer.data["description"], room_type.description)
        self.assertEqual(serializer.data["capacity"], room_type.capacity)
        self.assertEqual(
            str(serializer.data["price_per_night"]), str(room_type.price_per_night)
        )
        self.assertEqual(serializer.data["pet_type"], room_type.pet_type)
        self.assertEqual(serializer.data["hotel"], room_type.hotel.id)
