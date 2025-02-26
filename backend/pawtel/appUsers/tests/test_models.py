from django.test import TestCase
from appUsers.models import AppUser
from django.core.exceptions import ValidationError

class AppUserModelTest(TestCase):

    def test_create_valid_appuser(self):
        """Creación de un AppUser válido"""
        user = AppUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            phone="+34987654321",
            password="securepassword123"
        )
        self.assertEqual(user.username, "pepe")
        self.assertEqual(user.email, "pepe@example.com")
        self.assertEqual(user.phone, "+34987654321")

    def test_create_appuser_invalid_email(self):
        """Intenta crear un AppUser con un email inválido"""
        with self.assertRaises(ValidationError):
            user = AppUser.objects.create_user(
                username="pepito",
                email="invalid-email",
                phone="+34987654321",
                password="securepassword123"
            )
            user.full_clean()  # Valida las restricciones antes de guardar

    def test_create_appuser_invalid_phone(self):
        """Intenta crear un AppUser con un número de teléfono inválido"""
        with self.assertRaises(ValidationError):
            user = AppUser.objects.create_user(
                username="jhonny",
                email="validemail@example.com",
                phone="123456789",  
                password="securepassword"
            )
            user.full_clean()

    def test_create_appuser_duplicate_email(self):
        """Intenta crear un AppUser con un email duplicado"""
        AppUser.objects.create_user(
            username="user1",
            email="duplicate@example.com",
            phone="+34987654321",
            password="securepass"
        )
        with self.assertRaises(ValidationError):
            user = AppUser.objects.create_user(
                username="user2",
                email="duplicate@example.com",  # Email ya registrado
                phone="+34987654322",
                password="securepass12"
            )
            user.full_clean()

    def test_create_appuser_blank_email(self):
        """Intenta crear un AppUser sin email"""
        with self.assertRaises(ValidationError):
            user = AppUser.objects.create_user(
                username="noemailuser",
                email="",
                phone="+34987654321",
                password="securepassword123"
            )
            user.full_clean()

    def test_create_appuser_blank_phone(self):
        """Intenta crear un AppUser sin número de teléfono"""
        with self.assertRaises(ValidationError):
            user = AppUser.objects.create_user(
                username="nophoneuser",
                email="nophone@example.com",
                phone="",
                password="securepassword123"
            )
            user.full_clean()