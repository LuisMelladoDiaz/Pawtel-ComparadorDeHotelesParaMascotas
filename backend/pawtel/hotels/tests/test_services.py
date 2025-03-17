from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.hotels.services import HotelService
from pawtel.room_types.models import RoomType
from rest_framework.exceptions import PermissionDenied


class HotelServiceTest(TestCase):
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
            name="Test Hotel", is_archived=False, hotel_owner=self.hotel_owner
        )
        self.archived_hotel = Hotel.objects.create(
            name="Archived Hotel", is_archived=True, hotel_owner=self.hotel_owner
        )

        self.room_type1 = RoomType.objects.create(
            name="Single",
            hotel=self.hotel,
            description="A cozy single room.",
            capacity=1,
            price_per_night=50.0,
            pet_type="DOG",
        )

        self.room_type2 = RoomType.objects.create(
            name="Double",
            hotel=self.hotel,
            description="A spacious double room.",
            capacity=2,
            price_per_night=75.0,
            pet_type="CAT",
        )

        self.customer_user = AppUser.objects.create_user(
            username="customer1",
            email="customer@example.com",
            password="testpassword123",
            phone="+34987652321",
        )
        self.customer = Customer.objects.create(user_id=self.customer_user.id)

        self.hotel_owner_user = AppUser.objects.create_user(
            username="hotelowner2",
            email="owner2@example.com",
            password="testpassword123",
            phone="+34984654321",
        )
        self.hotel_owner = HotelOwner.objects.create(user_id=self.hotel_owner_user.id)

    def test_get_all_room_types_of_hotel(self):
        room_types = HotelService.get_all_room_types_of_hotel(self.hotel.id)
        self.assertEqual(len(room_types), 2)
        self.assertEqual(room_types[0].name, "Single")
        self.assertEqual(room_types[1].name, "Double")

    def test_customer_allowed_actions(self):
        allowed_actions = ["list", "retrieve", "get_all_room_types_of_hotel"]
        for action in allowed_actions:
            result, user_type = HotelService.check_permission(
                self.customer_user, action
            )
            self.assertTrue(result)
            self.assertEqual(user_type, "Customer")

    def test_customer_denied_actions(self):
        denied_actions = ["create", "update", "destroy", "get_bookings_of_hotel"]
        for action in denied_actions:
            with self.assertRaises(PermissionDenied):
                HotelService.check_permission(self.customer_user, action)

    def test_hotel_owner_allowed_actions(self):
        allowed_actions = [
            "list",
            "retrieve",
            "create",
            "update",
            "destroy",
            "get_all_room_types_of_hotel",
            "get_bookings_of_hotel",
        ]
        for action in allowed_actions:
            result, user_type = HotelService.check_permission(
                self.hotel_owner_user, action
            )
            self.assertTrue(result)
            self.assertEqual(user_type, "HotelOwner")
