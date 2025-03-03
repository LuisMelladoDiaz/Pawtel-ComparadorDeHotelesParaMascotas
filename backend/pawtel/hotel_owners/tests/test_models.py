from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from pawtel.hotel_owners.models import HotelOwner


class HotelOwnerModelTest(TestCase):

    def test_create_valid_hotel_owner(self):
        owner = HotelOwner.objects.create_user(
            username="hotelowner1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.assertEqual(owner.username, "hotelowner1")
        self.assertEqual(owner.first_name, "John")
        self.assertEqual(owner.last_name, "Doe")
        self.assertEqual(owner.email, "owner@example.com")
        self.assertEqual(owner.phone, "+34987654321")
        self.assertTrue(owner.check_password("securepassword123"))
        self.assertTrue(owner.is_active)
        self.assertFalse(owner.is_staff)
        self.assertFalse(owner.is_superuser)

    def test_create_hotel_owner_invalid_username(self):
        invalid_usernames = ["", "A" * 151]

        for username in invalid_usernames:
            with self.subTest(username=username):
                owner = HotelOwner(
                    username=username,
                    first_name="John",
                    last_name="Doe",
                    email="owner@example.com",
                    phone="+34987654321",
                    password="securepassword123",
                )
                with self.assertRaises(ValidationError):
                    owner.full_clean()

    def test_create_hotel_owner_duplicate_username(self):
        HotelOwner.objects.create_user(
            username="owner1",
            first_name="John",
            last_name="Doe",
            email="owner1@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        with self.assertRaises(IntegrityError):
            HotelOwner.objects.create_user(
                username="owner1",
                first_name="Jane",
                last_name="Smith",
                email="owner2@example.com",
                phone="+34987654322",
                password="securepassword123",
            )

    def test_create_hotel_owner_invalid_phone(self):
        invalid_phones = ["123456789", "not-a-phone", "A" * 14]

        for phone in invalid_phones:
            with self.subTest(phone=phone):
                owner = HotelOwner(
                    username="hotelowner2",
                    first_name="John",
                    last_name="Doe",
                    email="valid@example.com",
                    phone=phone,
                    password="securepassword123",
                )
                with self.assertRaises(ValidationError):
                    owner.full_clean()

    def test_create_hotel_owner_duplicate_phone(self):
        HotelOwner.objects.create_user(
            username="owner1",
            first_name="John",
            last_name="Doe",
            email="owner1@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        with self.assertRaises(IntegrityError):
            HotelOwner.objects.create_user(
                username="owner2",
                first_name="Jane",
                last_name="Smith",
                email="owner2@example.com",
                phone="+34987654321",
                password="securepassword123",
            )

    def test_create_hotel_owner_invalid_email(self):
        invalid_emails = ["invalid-email", "", "A" * 101]

        for email in invalid_emails:
            with self.subTest(email=email):
                owner = HotelOwner(
                    username="hotelowner3",
                    first_name="John",
                    last_name="Doe",
                    email=email,
                    phone="+34987654321",
                    password="securepassword123",
                )
                with self.assertRaises(ValidationError):
                    owner.full_clean()

    def test_create_hotel_owner_duplicate_email(self):
        HotelOwner.objects.create_user(
            username="owner1",
            first_name="John",
            last_name="Doe",
            email="duplicate@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        with self.assertRaises(IntegrityError):
            HotelOwner.objects.create_user(
                username="owner2",
                first_name="Jane",
                last_name="Smith",
                email="duplicate@example.com",
                phone="+34987654322",
                password="securepassword123",
            )
