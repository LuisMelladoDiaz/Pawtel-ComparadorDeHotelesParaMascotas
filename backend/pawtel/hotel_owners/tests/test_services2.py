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
    def create_app_user(self, username, email, phone, password, is_active=True):
        return AppUser.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            is_active=is_active,
        )

    def create_hotel_owner(self, user):
        return HotelOwner.objects.create(user_id=user.id)

    def create_hotel(self, name, owner, address, city, description="Desc"):
        return Hotel.objects.create(
            name=name,
            hotel_owner=owner,
            address=address,
            city=city,
            description=description,
        )

    def create_room_type(
        self, hotel, name, capacity, num_rooms, price_per_night, pet_type
    ):
        return RoomType.objects.create(
            hotel=hotel,
            name=name,
            description="Habitación para mascotas",
            capacity=capacity,
            num_rooms=num_rooms,
            price_per_night=price_per_night,
            pet_type=pet_type,
            is_archived=False,
        )

    def setUp(self):
        self.client = APIClient()

        self.authenticated_user = self.create_app_user(
            "authenticated_user",
            "authenticated_user@example.com",
            "+34111222333",
            "123456",
        )
        self.authenticated_hotel_owner = self.create_hotel_owner(
            self.authenticated_user
        )
        self.client.force_authenticate(user=self.authenticated_user)

        self.inactive_app_user = self.create_app_user(
            "inactive_owner",
            "inactive_owner@example.com",
            "+34123456788",
            "123456",
            is_active=False,
        )
        self.inactive_hotel_owner = self.create_hotel_owner(self.inactive_app_user)

        self.hotel1 = self.create_hotel(
            "Hotel 1", self.authenticated_hotel_owner, "Calle 1", "Ciudad1"
        )
        self.hotel2 = self.create_hotel(
            "Hotel 2", self.authenticated_hotel_owner, "Calle 2", "Ciudad2"
        )

        self.room_type1 = self.create_room_type(
            self.hotel1, "RoomType 1", 10, 5, 100.00, PetType.DOG
        )

        self.user_customer = self.create_app_user(
            "customer_user", "customer@example.com", "+34987654321", "password123"
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

        HotelOwnerService.validate_all_hotels_deletion(
            self.authenticated_hotel_owner.id
        )

        self.room_type1.refresh_from_db()
        self.hotel1.refresh_from_db()
        self.assertTrue(self.hotel1.is_archived)
        self.assertTrue(self.room_type1.is_archived)
