from django.test import TestCase
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import PermissionDenied


class HotelServiceTest(TestCase):
    def setUp(self):
        self.hotel_owner = HotelOwner.objects.create(
            username="owner_test",
            email="owner@example.com",
            password="securepassword123",
            phone="+1234567890",
            is_active=True,
        )
        self.hotel1 = Hotel.objects.create(name="Hotel 1", hotel_owner=self.hotel_owner)
        self.hotel2 = Hotel.objects.create(name="Hotel 2", hotel_owner=self.hotel_owner)

        self.inactive_owner = HotelOwner.objects.create(
            username="inactive_owner",
            email="inactive_owner@example.com",
            password="securepassword123",
            phone="+0987654321",
            is_active=False,
        )
        self.inactive_hotel = Hotel.objects.create(
            name="Inactive Hotel", hotel_owner=self.inactive_owner
        )

    def test_get_all_hotels_by_hotel_owner(self):
        hotels_data = HotelOwnerService.get_all_hotels_of_hotel_owner(
            self.hotel_owner.id
        )
        self.assertEqual(len(hotels_data), 2)
        self.assertEqual(hotels_data[0].name, "Hotel 1")
        self.assertEqual(hotels_data[1].name, "Hotel 2")

    def test_delete_all_hotels_by_hotel_owner(self):
        hotels_deleted = HotelOwnerService.delete_all_hotels_of_hotel_owner(
            self.hotel_owner.id
        )
        self.assertEqual(hotels_deleted, 2)
        self.assertEqual(Hotel.objects.filter(hotel_owner=self.hotel_owner).count(), 0)

    def test_check_if_active(self):
        try:
            HotelOwnerService.check_if_active(self.hotel_owner.id)
        except PermissionDenied:
            self.fail(
                "check_if_active raised an unexpected exception for an active owner."
            )
        with self.assertRaises(PermissionDenied):
            HotelOwnerService.check_if_active(self.inactive_owner.id)
