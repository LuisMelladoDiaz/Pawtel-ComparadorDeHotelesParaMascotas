from django.test import TestCase
from datetime import date, timedelta
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.hotels.models import Hotel
from pawtel.hotel_owners.models import HotelOwner
from pawtel.room_types.models import RoomType
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer


class BookingSerializerTest(TestCase):

    def setUp(self):
        self.app_user_customer = AppUser.objects.create_user(
            username="customer11",
            first_name="Dani",
            last_name="Johnson",
            email="dani@example.com",
            phone="+34987654333",
            password="butarque",
        )
        self.app_user_hotel_owner = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="Juan",
            last_name="Smith",
            email="bob@example.com",
            phone="+34987654322",
            password="urepassword123",
        )

        self.customer = Customer.objects.create(user=self.app_user_customer)
        self.hotel_owner = HotelOwner.objects.create(user=self.app_user_hotel_owner)

        self.hotel = Hotel.objects.create(
            name="Laibe",
            address="Calle 46",
            city="Barcelona",
            description="Un hotel exclusivo",
            hotel_owner=self.hotel_owner,
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite Ejecutiva",
            description="Habitación con vista al mar.",
            capacity=2,
            price_per_night=200.00,
            pet_type="DOG",
        )

        self.valid_data = {
            "customer": self.customer.id,
            "room_type": self.room_type.id,
            "start_date": str(date.today() + timedelta(days=2)),
            "end_date": str(date.today() + timedelta(days=5)),
            "total_price": 600.00
        }

    # POST tests --------------------------------------------------------------

    def test_valid_post_request(self):
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = BookingSerializer(data=self.valid_data, context=context)
        self.assertTrue(serializer.is_valid())

    def test_missing_required_fields_post(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("start_date")  # Se elimina `start_date`
        context = {"request": type("Request", (), {"method": "POST"})}
        serializer = BookingSerializer(data=invalid_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("start_date", serializer.errors)

    # PUT tests --------------------------------------------------------------

    def test_ignore_all_fields_for_put(self):
        data = self.valid_data.copy()
        data["id"] = 99
        data["customer"] = "invalid..."

        context = {"request": type("Request", (), {"method": "PUT"})}
        serializer = BookingSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("customer", serializer.validated_data)

    # PATCH tests ------------------------------------------------------------

    def test_ignore_all_fields_for_patch(self):
        data = self.valid_data.copy()
        data["id"] = 99
        data["customer"] = "invalid..."

        context = {"request": type("Request", (), {"method": "PATCH"})}
        serializer = BookingSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("customer", serializer.validated_data)

    # GET tests --------------------------------------------------------------

    def test_serializer_get_method(self):
        booking = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=5),
            total_price=600.00
        )
        context = {"request": type("Request", (), {"method": "GET"})}
        serializer = BookingSerializer(booking, context=context)

        self.assertIn("customer", serializer.data)
        self.assertIn("room_type", serializer.data)
        self.assertEqual(serializer.data["customer"], self.customer.id)
        self.assertEqual(serializer.data["room_type"], self.room_type.id)

  
