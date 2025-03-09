from django.test import TestCase
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import PermissionDenied


class HotelOwnerServiceTest(TestCase):
    def test_get_all_hotels_of_hotel_owner(self):
        hotel_owner = HotelOwner.objects.create(
            email="test@example.com", phone="123456789", is_active=True
        )
        hotel1 = Hotel.objects.create(
            name="Hotel One", hotel_owner=hotel_owner, is_archived=False
        )
        hotel2 = Hotel.objects.create(
            name="Hotel Two", hotel_owner=hotel_owner, is_archived=False
        )
        hotel_archived = Hotel.objects.create(
            name="Hotel Archived", hotel_owner=hotel_owner, is_archived=True
        )
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(hotel_owner.id)
        self.assertListEqual(list(hotels), [hotel1, hotel2])
        self.assertNotIn(hotel_archived, hotels)

    def test_get_all_hotels_of_hotel_owner_no_hotels(self):
        hotel_owner = HotelOwner.objects.create(
            email="empty@example.com", phone="987654321", is_active=True
        )
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(hotel_owner.id)
        self.assertListEqual(list(hotels), [])

    def test_delete_all_hotels_of_hotel_owner(self):
        hotel_owner = HotelOwner.objects.create(
            email="delete@example.com", phone="1122334455", is_active=True
        )
        Hotel.objects.create(name="Hotel A", hotel_owner=hotel_owner, is_archived=False)
        Hotel.objects.create(name="Hotel B", hotel_owner=hotel_owner, is_archived=False)
        HotelOwnerService.delete_all_hotels_of_hotel_owner(hotel_owner.id)
        hotels = Hotel.objects.filter(hotel_owner=hotel_owner)
        self.assertEqual(hotels.count(), 0)

    def test_delete_all_hotels_of_hotel_owner_no_hotels(self):
        hotel_owner = HotelOwner.objects.create(
            email="nohotels@example.com", phone="5566778899", is_active=True
        )
        with self.assertRaises(PermissionDenied, msg="No hotels to delete."):
            HotelOwnerService.delete_all_hotels_of_hotel_owner(hotel_owner.id)
