from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import PermissionDenied


class HotelOwnerServiceTest(TestCase):

    def setUp(self):
        self.app_user = AppUser.objects.create(
            username="active_owner",
            email="active_owner@example.com",
            phone="+34123456789",
            password="123456",
            is_active=True,
        )
        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user.id)

    def test_list_hotels_of_hotel_owner(self):
        hotel1 = Hotel.objects.create(
            name="Hotel One", hotel_owner=self.hotel_owner, is_archived=False
        )
        hotel2 = Hotel.objects.create(
            name="Hotel Two", hotel_owner=self.hotel_owner, is_archived=False
        )
        hotel_archived = Hotel.objects.create(
            name="Hotel Archived", hotel_owner=self.hotel_owner, is_archived=True
        )
        hotels = HotelOwnerService.list_hotels_of_hotel_owner(self.hotel_owner.id)
        self.assertListEqual(list(hotels), [hotel1, hotel2])
        self.assertNotIn(hotel_archived, hotels)

    def test_list_hotels_of_hotel_owner_no_hotels(self):
        hotels = HotelOwnerService.list_hotels_of_hotel_owner(self.hotel_owner.id)
        self.assertListEqual(list(hotels), [])

    def test_delete_all_hotels_of_hotel_owner(self):
        Hotel.objects.create(
            name="Hotel A", hotel_owner=self.hotel_owner, is_archived=False
        )
        Hotel.objects.create(
            name="Hotel B", hotel_owner=self.hotel_owner, is_archived=False
        )
        HotelOwnerService.delete_all_hotels_of_hotel_owner(self.hotel_owner.id)
        hotels = Hotel.objects.filter(hotel_owner=self.hotel_owner)
        self.assertEqual(hotels.count(), 0)

    def test_delete_all_hotels_of_hotel_owner_no_hotels(self):
        with self.assertRaises(PermissionDenied, msg="No hotels to delete."):
            HotelOwnerService.delete_all_hotels_of_hotel_owner(self.hotel_owner.id)

    def test_approve_hotel_owner_patch(self):
        # Ejecutar el método del servicio
        updated_owner = HotelOwnerService.approve_hotel_owner(self.hotel_owner.id)

        # Verificar que se ha aprobado
        self.assertTrue(updated_owner.is_approved)
