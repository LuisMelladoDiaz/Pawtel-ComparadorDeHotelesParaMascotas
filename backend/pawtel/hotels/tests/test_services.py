from datetime import date, timedelta
from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.bookings.models import Booking
from pawtel.hotels.services import HotelService
from pawtel.room_types.models import RoomType


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
        
        
        self.app_user_owner2 = AppUser.objects.create_user(
            username="hotelowner2",
            first_name="Alice",
            last_name="Smith",
            email="owner2@example.com",
            phone="+34987654322",
            password="securepassword123",
        )

        self.hotel_owner2 = HotelOwner.objects.create(user_id=self.app_user_owner2.id)

        self.hotel2 = Hotel.objects.create(
            name="Hotel Luna Azul",
            is_archived=False,
            hotel_owner=self.hotel_owner2,
        )

        self.room_type3 = RoomType.objects.create(
            name="Suite",
            hotel=self.hotel2,
            description="Luxury suite",
            capacity=2,
            price_per_night=200.0,
            pet_type="CAT",
        )

        self.booking1 = Booking.objects.create(
            customer=self.hotel_owner,
            room_type=self.room_type1,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=7),
            total_price=400.00,
        )

        self.booking2 = Booking.objects.create(
            customer=self.hotel_owner2,
            room_type=self.room_type3,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=10),
            total_price=1000.00,
        )

    def test_get_all_bookings_by_hotel(self):
        bookings = HotelService.get_all_bookings_by_hotel(self.hotel.id)
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0].id, self.booking1.id)

    def test_get_all_room_types_of_hotel(self):
        room_types = HotelService.get_all_room_types_of_hotel(self.hotel.id)
        self.assertEqual(len(room_types), 2)
        self.assertEqual(room_types[0].name, "Single")
        self.assertEqual(room_types[1].name, "Double")
        
        

