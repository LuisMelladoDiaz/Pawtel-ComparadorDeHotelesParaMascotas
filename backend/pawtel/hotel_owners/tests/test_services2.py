from datetime import date, timedelta

from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient


class HotelOwnerViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.authenticated_user = AppUser.objects.create_user(
            username="authenticated_user",
            email="authenticated_user@example.com",
            phone="+34111222333",
            password="123456",
            is_active=True,
        )
        self.authenticated_hotel_owner = HotelOwner.objects.create(
            user_id=self.authenticated_user.id
        )
        self.client.force_authenticate(user=self.authenticated_user)

        self.inactive_app_user = AppUser.objects.create(
            username="inactive_owner",
            email="inactive_owner@example.com",
            phone="+34123456788",
            password="123456",
            is_active=False,
        )
        self.inactive_hotel_owner = HotelOwner.objects.create(
            user_id=self.inactive_app_user.id
        )
        self.hotel1 = Hotel.objects.create(
            name="Hotel 1",
            hotel_owner=self.authenticated_hotel_owner,
            address="Calle 1",
            city="Ciudad1",
            description="Desc",
        )
        self.hotel2 = Hotel.objects.create(
            name="Hotel 2",
            hotel_owner=self.authenticated_hotel_owner,
            address="Calle 2",
            city="Ciudad2",
            description="Desc",
        )
        self.room_type1 = RoomType.objects.create(
            hotel=self.hotel1,
            name="RoomType 1",
            description="Habitación para mascotas",
            capacity=10,
            num_rooms=5,
            price_per_night=100.00,
            pet_type=PetType.DOG,
            is_archived=False,
        )
        self.user_customer = AppUser.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            phone="+34987654321",
            password="password123",
        )
        self.customer = Customer.objects.create(user=self.user_customer)

    def test_validate_all_hotels_deletion_without_booking(self):
        try:
            HotelOwnerService.validate_all_hotels_deletion(
                self.authenticated_hotel_owner.id
            )
        except ValidationError:
            self.fail(
                "validate_all_hotels_deletion lanzó ValidationError sin bookings."
            )

    def test_validate_all_hotels_deletion_with_future_booking(self):
        future_start = date.today() + timedelta(days=10)
        future_end = future_start + timedelta(days=5)
        Booking.objects.create(
            room_type=self.room_type1,
            customer=self.customer,
            start_date=future_start,
            end_date=future_end,
            total_price=100.00,
        )

        with self.assertRaises(ValidationError) as context:
            HotelOwnerService.validate_all_hotels_deletion(
                self.authenticated_hotel_owner.id
            )
        error_message = (
            context.exception.detail
            if hasattr(context.exception, "detail")
            else context.exception.args[0]
        )
        self.assertEqual(
            error_message, ["Cannot delete because there is an upcoming booking."]
        )

    def test_validate_all_hotels_deletion_with_past_booking(self):
        today = date.today()
        past_start = today - timedelta(days=100)
        past_end = past_start + timedelta(days=5)
        Booking.objects.create(
            room_type=self.room_type1,
            customer=self.customer,
            start_date=past_start,
            end_date=past_end,
            total_price=100.00,
        )
        with self.assertRaises(ValidationError) as context:
            HotelOwnerService.validate_all_hotels_deletion(
                self.authenticated_hotel_owner.id
            )
        error_message = (
            context.exception.detail
            if hasattr(context.exception, "detail")
            else context.exception.args[0]
        )
        self.assertEqual(
            error_message,
            [
                "Cannot delete because there are bookings in the past 3 years. It has been archived instead."
            ],
        )
        self.room_type1.refresh_from_db()
        self.assertTrue(self.room_type1.is_archived)
