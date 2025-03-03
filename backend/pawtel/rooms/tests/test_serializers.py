from django.test import TestCase
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType
from pawtel.rooms.models import Room
from pawtel.rooms.serializers import RoomSerializer


class RoomSerializerTest(TestCase):

    def setUp(self):
        # Creamos un HotelOwner para asignarlo al Hotel
        self.hotel_owner = HotelOwner.objects.create_user(
            username="hotelowner1",
            first_name="Owner",
            last_name="Test",
            email="hotelowner1@example.com",
            phone="+34111222333",
            password="securepassword123",
        )
        # Creamos un Hotel para asignarlo al RoomType
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="123 Test Street",
            city="Test City",
            description="Hotel de prueba",
            hotel_owner=self.hotel_owner,
        )
        # Creamos un RoomType para asignarlo a Room
        self.room_type = RoomType.objects.create(
            name="Suite",
            description="Habitación de lujo",
            capacity=2,
            price_per_night="120.00",
            pet_type=PetType.DOG,
            hotel=self.hotel,
        )
        # Datos válidos para Room
        self.valid_data = {
            "name": "Room A",
            "room_type": self.room_type.id,
        }

    # POST tests -------------------------------------------------------------

    def test_serializer_valid_data_post(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], self.valid_data["name"])

    def test_serializer_missing_required_field_post(self):
        # Caso: Falta el campo "name"
        invalid_data = self.valid_data.copy()
        invalid_data.pop("name")
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

        # Caso: Falta el campo "room_type"
        invalid_data = self.valid_data.copy()
        invalid_data.pop("room_type")
        serializer = RoomSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("room_type", serializer.errors)

    def test_invalid_name_length_post(self):
        # Exceder la longitud máxima de 50 caracteres en "name"
        invalid_data = self.valid_data.copy()
        invalid_data["name"] = "a" * 51
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_ignore_additional_fields_for_post(self):
        # Se agregan campos adicionales que deben ser ignorados
        data = self.valid_data.copy()
        data["is_archived"] = True
        data["extra_field"] = "valor extra"
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("extra_field", serializer.validated_data)

    # PUT tests --------------------------------------------------------------

    def test_serializer_valid_data_put(self):
        context = {"request": type("Request", (), {"method": "PUT"})}
        serializer = RoomSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_ignore_additional_fields_for_put(self):
        # En PUT solo se deben considerar los campos editables (en este caso, solo "name")
        data = self.valid_data.copy()
        data["is_archived"] = True
        data["room_type"] = None  # No es editable en PUT
        data["extra_field"] = "valor extra"
        context = {"request": type("Request", (), {"method": "PUT"})}
        serializer = RoomSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("room_type", serializer.validated_data)
        self.assertNotIn("extra_field", serializer.validated_data)

    # PATCH tests ------------------------------------------------------------

    def test_serializer_valid_data_patch(self):
        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = RoomSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_ignore_additional_fields_for_patch(self):
        # En PATCH solo se deben procesar los campos editables
        data = {
            "name": "Room A Updated",
            "is_archived": True,
            "room_type": self.room_type.id,  # No es editable en PATCH
            "extra_field": "valor extra",
        }
        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = RoomSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], data["name"])
        self.assertNotIn("is_archived", serializer.validated_data)
        self.assertNotIn("room_type", serializer.validated_data)
        self.assertNotIn("extra_field", serializer.validated_data)

    # GET tests --------------------------------------------------------------

    def test_serializer_get_method(self):
        # Se crea una instancia de Room y se serializa en GET
        room = Room.objects.create(
            name=self.valid_data["name"],
            room_type=self.room_type,
        )
        context = {"request": type("Request", (), {"method": "GET"})}
        serializer = RoomSerializer(room, context=context)
        self.assertEqual(serializer.data["name"], room.name)
        self.assertEqual(serializer.data["room_type"], room.room_type.id)
        self.assertIn("id", serializer.data)
        self.assertIn("is_archived", serializer.data)

    # Creación y guardado de instancias ---------------------------------------

    def test_create_room_instance_from_json(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # Se crea pero no se guarda la instancia en la BD
        room = serializer.create(serializer.validated_data)
        self.assertEqual(room.name, self.valid_data["name"])
        self.assertEqual(room.room_type.id, self.valid_data["room_type"])

    def test_save_room_instance_from_json(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = RoomSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # Se crea y guarda la instancia en la BD
        room = serializer.save()
        self.assertEqual(room.name, self.valid_data["name"])
        self.assertEqual(room.room_type.id, self.valid_data["room_type"])

    def test_serialize_room_instance_to_json(self):
        room = Room.objects.create(
            name=self.valid_data["name"],
            room_type=self.room_type,
        )
        serializer = RoomSerializer(room)
        self.assertEqual(serializer.data["name"], room.name)
        self.assertEqual(serializer.data["room_type"], room.room_type.id)
