from django.test import TestCase
from pawtel.app_users.models import AppUser
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.hotels.services import HotelService
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room


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

        Room.objects.create(room_type=self.room_type1)
        Room.objects.create(room_type=self.room_type2)
        Room.objects.create(room_type=self.room_type2)

    def test_get_all_room_types_of_hotel(self):
        room_types = HotelService.get_all_room_types_of_hotel(self.hotel.id)
        self.assertEqual(len(room_types), 2)
        self.assertEqual(room_types[0].name, "Single")
        self.assertEqual(room_types[1].name, "Double")

    def test_get_total_vacancy_for_each_room_type_of_hotel(self):
        vacancies = HotelService.get_total_vacancy_for_each_room_type_of_hotel(
            self.hotel.id
        )
        self.assertEqual(len(vacancies), 2)

        single_vacancy = next(
            v for v in vacancies if v["room_type_id"] == self.room_type1.id
        )
        double_vacancy = next(
            v for v in vacancies if v["room_type_id"] == self.room_type2.id
        )

        self.assertEqual(single_vacancy["total_vacancy"], 1)
        self.assertEqual(double_vacancy["total_vacancy"], 4)

    def test_get_total_vacancy_for_each_room_type_of_hotel_no_rooms(self):
        hotel_no_rooms = Hotel.objects.create(
            name="Hotel with No Rooms", is_archived=False, hotel_owner=self.hotel_owner
        )
        vacancies = HotelService.get_total_vacancy_for_each_room_type_of_hotel(
            hotel_no_rooms.id
        )
        self.assertEqual(len(vacancies), 0)
