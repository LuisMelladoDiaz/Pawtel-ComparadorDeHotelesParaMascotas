from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from pawtel.app_users.models import AppUser


class AppUserModelTest(TestCase):

    def test_create_valid_app_user(self):
        owner = AppUser.objects.create_user(
            username="appuser1",
            first_name="John",
            last_name="Doe",
            email="owner@example.com",
            phone="+34987654321",
            password="securepassword123",
        )
        self.assertEqual(owner.username, "appuser1")
        self.assertEqual(owner.first_name, "John")
        self.assertEqual(owner.last_name, "Doe")
        self.assertEqual(owner.email, "owner@example.com")
        self.assertEqual(owner.phone, "+34987654321")
        self.assertTrue(owner.check_password("securepassword123"))
        self.assertTrue(owner.is_active)
        self.assertFalse(owner.is_staff)
        self.assertFalse(owner.is_superuser)

    def test_create_app_user_invalid_username(self):
        invalid_usernames = ["", "A" * 151]

        for username in invalid_usernames:
            with self.subTest(username=username):
                owner = AppUser(
                    username=username,
                    first_name="John",
                    last_name="Doe",
                    email="owner@example.com",
                    phone="+34987654321",
                    password="securepassword123",
                )
                with self.assertRaises(ValidationError):
                    owner.full_clean()

    def test_create_app_user_duplicate_username(self):
        AppUser.objects.create_user(
            username="owner1",
            first_name="John",
            last_name="Doe",
            email="owner1@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        with self.assertRaises(IntegrityError):
            AppUser.objects.create_user(
                username="owner1",
                first_name="Jane",
                last_name="Smith",
                email="owner2@example.com",
                phone="+34987654322",
                password="securepassword123",
            )

    def test_create_app_user_invalid_phone(self):
        invalid_phones = ["123456789", "not-a-phone", "A" * 14]

        for phone in invalid_phones:
            with self.subTest(phone=phone):
                owner = AppUser(
                    username="appuser2",
                    first_name="John",
                    last_name="Doe",
                    email="valid@example.com",
                    phone=phone,
                    password="securepassword123",
                )
                with self.assertRaises(ValidationError):
                    owner.full_clean()

    def test_create_app_user_duplicate_phone(self):
        AppUser.objects.create_user(
            username="owner1",
            first_name="John",
            last_name="Doe",
            email="owner1@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        with self.assertRaises(IntegrityError):
            AppUser.objects.create_user(
                username="owner2",
                first_name="Jane",
                last_name="Smith",
                email="owner2@example.com",
                phone="+34987654321",
                password="securepassword123",
            )

    def test_create_app_user_invalid_email(self):
        invalid_emails = ["invalid-email", "", "A" * 101]

        for email in invalid_emails:
            with self.subTest(email=email):
                owner = AppUser(
                    username="appuser3",
                    first_name="John",
                    last_name="Doe",
                    email=email,
                    phone="+34987654321",
                    password="securepassword123",
                )
                with self.assertRaises(ValidationError):
                    owner.full_clean()

    def test_create_app_user_duplicate_email(self):
        AppUser.objects.create_user(
            username="owner1",
            first_name="John",
            last_name="Doe",
            email="duplicate@example.com",
            phone="+34987654321",
            password="securepassword123",
        )

        with self.assertRaises(IntegrityError):
            AppUser.objects.create_user(
                username="owner2",
                first_name="Jane",
                last_name="Smith",
                email="duplicate@example.com",
                phone="+34987654322",
                password="securepassword123",
            )
