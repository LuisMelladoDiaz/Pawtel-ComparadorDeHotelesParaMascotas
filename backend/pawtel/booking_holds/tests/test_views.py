from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta
from pawtel.app_admins.models import App_Admin
from pawtel.app_users.models import AppUser
from pawtel.booking_holds.models import BookingHold
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from rest_framework import status
from rest_framework.test import APIClient


class BookingHoldViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client2 = APIClient()
        self.admin_user = AppUser.objects.create_user(
            username="admin1",
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            phone="+34987654221",
            password="securepassword123",
        )
        self.admin = App_Admin.objects.create(user=self.admin_user)
        self.client2.force_authenticate(user=self.admin_user)

        self.app_user_owner = AppUser.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.hotel_owner = HotelOwner.objects.create(user_id=self.app_user_owner.id)
        self.hotel = Hotel.objects.create(
            name="Test Hotel", is_archived=False, hotel_owner=self.hotel_owner
        )

        self.app_user_customer = AppUser.objects.create_user(
            username="customer1",
            first_name="John",
            last_name="Doe",
            email="customer@example.com",
            phone="+34123456789",
            password="securepassword123",
        )
        self.customer = Customer.objects.create(user_id=self.app_user_customer.id)

        self.client.force_authenticate(user=self.app_user_customer)

        self.archived_hotel = Hotel.objects.create(
            name="Archived Hotel", is_archived=True, hotel_owner=self.hotel_owner
        )

        self.in_ten_minutes = now() + timedelta(minutes=10)

        self.room_type_unavailable_from_2_to_4 = RoomType.objects.create(
            name="Single",
            hotel=self.hotel,
            description="A cozy single room.",
            capacity=2,
            num_rooms=1,
            price_per_night=50.0,
            pet_type="DOG",
        )
        self.active_booking_hold = BookingHold.objects.create(
            customer=self.customer,
            room_type=self.room_type_unavailable_from_2_to_4,
            hold_expires_at=self.in_ten_minutes,
            booking_start_date=date.today() + timedelta(days=2),
            booking_end_date=date.today() + timedelta(days=4),
        )
        self.booking1 = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type_unavailable_from_2_to_4,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
            total_price=750.00,
        )

        self.room_type_no_holds = RoomType.objects.create(
            name="Double",
            hotel=self.hotel,
            description="A spacious double room.",
            capacity=1,
            num_rooms=1,
            price_per_night=75.0,
            pet_type="CAT",
        )

    # GET --------------------------------------------------------------------

    def test_list_booking_holds(self):
        url = reverse("booking-hold-list")
        response = self.client2.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_booking_hold(self):
        url = reverse("booking-hold-detail", kwargs={"pk": self.active_booking_hold.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["room_type"], self.room_type_unavailable_from_2_to_4.id
        )

    # POST -------------------------------------------------------------------

    def test_create_booking_hold_with_existing_inactive_hold(self):
        url = reverse("booking-hold-list")
        data = {
            "room_type": self.room_type_no_holds.id,
            "booking_start_date": str(date.today() + timedelta(days=3)),
            "booking_end_date": str(date.today() + timedelta(days=7)),
        }

        # Deactive currently active booking hold by setting expiration to past
        self.active_booking_hold.hold_expires_at = now() - timedelta(minutes=5)
        self.active_booking_hold.save()

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            BookingHold.objects.filter(room_type=self.room_type_no_holds).exists()
        )

    def test_create_booking_hold_ignores_expires_at(self):
        url = reverse("booking-hold-list")
        data = {
            "room_type": self.room_type_no_holds.id,
            "booking_start_date": str(date.today() + timedelta(days=3)),
            "booking_end_date": str(date.today() + timedelta(days=7)),
            "hold_expires_at": str(
                date.today() - timedelta(days=200)
            ),  # should be ignored
        }

        # Deactive currently active booking hold by setting expiration to past
        self.active_booking_hold.hold_expires_at = now() - timedelta(minutes=5)
        self.active_booking_hold.save()

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            BookingHold.objects.filter(room_type=self.room_type_no_holds).exists()
        )

    def test_create_booking_hold_with_existing_active_hold(self):
        url = reverse("booking-hold-list")
        data = {
            "room_type": self.room_type_no_holds.id,
            "booking_start_date": str(date.today() + timedelta(days=3)),
            "booking_end_date": str(date.today() + timedelta(days=3)),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking_holds = BookingHold.objects.filter(
            room_type=self.room_type_no_holds
        ).all()
        self.assertEqual(len(booking_holds), 1)

    # test cannot create booking room type unavailable (use rt1 with 1 booking and 1 bookinghold)
    def test_create_booking_hold_invalid_with_unavailable_room_type(self):
        app_user_customer2 = AppUser.objects.create_user(
            username="customer2",
            first_name="John",
            last_name="Doe",
            email="customer2@example.com",
            phone="+987654321",
            password="securepassword123",
        )
        Customer.objects.create(user_id=app_user_customer2.id)
        self.client.force_authenticate(user=app_user_customer2)

        url = reverse("booking-hold-list")
        data = {
            "room_type": self.room_type_unavailable_from_2_to_4.id,
            "booking_start_date": str(date.today() + timedelta(days=2)),
            "booking_end_date": str(date.today() + timedelta(days=3)),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            not BookingHold.objects.filter(room_type=self.room_type_no_holds).exists()
        )

    # PUT/PATCH --------------------------------------------------------------

    def test_update_booking_hold_forbidden(self):
        url = reverse("booking-hold-detail", kwargs={"pk": self.active_booking_hold.id})
        data = {"booking_end_date": str(now().date() + timedelta(days=7))}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_booking_hold_forbidden(self):
        url = reverse("booking-hold-detail", kwargs={"pk": self.active_booking_hold.id})
        data = {"booking_end_date": str(now().date() + timedelta(days=7))}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE -----------------------------------------------------------------

    def test_delete_booking_hold(self):
        url = reverse("booking-hold-detail", kwargs={"pk": self.active_booking_hold.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            BookingHold.objects.filter(id=self.active_booking_hold.id).exists()
        )

    def test_delete_booking_hold_as_admin(self):
        url = reverse("booking-hold-detail", kwargs={"pk": self.active_booking_hold.id})
        response = self.client2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            BookingHold.objects.filter(id=self.active_booking_hold.id).exists()
        )
