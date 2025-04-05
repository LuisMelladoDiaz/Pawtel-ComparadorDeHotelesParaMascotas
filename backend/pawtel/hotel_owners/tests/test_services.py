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
        updated_owner = HotelOwnerService.approve_hotel_owner_patch(self.hotel_owner.id)
        self.assertTrue(updated_owner.is_approved)

    def test_delete_unapproved_hotel_owner(self):
        unapproved_user = AppUser.objects.create(
            username="to_delete",
            email="to_delete@example.com",
            phone="+34911112222",
            password="123456",
            is_active=True,
        )
        hotel_owner = HotelOwner.objects.create(user=unapproved_user, is_approved=False)

        HotelOwnerService.delete_unapproved_hotel_owner(hotel_owner.id)

        self.assertFalse(AppUser.objects.filter(id=unapproved_user.id).exists())
        self.assertFalse(HotelOwner.objects.filter(id=hotel_owner.id).exists())

    def test_list_unapproved_hotel_owners(self):

        unapproved1 = HotelOwner.objects.create(
            user=AppUser.objects.create(
                username="h1",
                email="h1@example.com",
                phone="+34111111111",
                password="123456",
            ),
            is_approved=False,
        )
        unapproved2 = HotelOwner.objects.create(
            user=AppUser.objects.create(
                username="h2",
                email="h2@example.com",
                phone="+34111111112",
                password="123456",
            ),
            is_approved=False,
        )
        approved = HotelOwner.objects.create(
            user=AppUser.objects.create(
                username="h3",
                email="h3@example.com",
                phone="+34111111113",
                password="123456",
            ),
            is_approved=True,
        )

        result = HotelOwnerService.list_unapproved_hotel_owners()
        self.assertIn(unapproved1, result)
        self.assertIn(unapproved2, result)
        self.assertNotIn(approved, result)
