from django.contrib.auth import get_user_model
from django.urls import reverse
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from rest_framework import status
from rest_framework.test import APITestCase


class UserInfoViewTest(APITestCase):
    def setUp(self):
        # Creamos un usuario para las pruebas
        self.user1 = get_user_model().objects.create_user(
            username="User1",
            email="user1@example.com",
            phone="+345678900",
            password="testpassword",
        )
        self.user2 = get_user_model().objects.create_user(
            username="User2",
            email="user2@example.com",
            phone="+347668400",
            password="testpassword",
        )
        # Define la URL del endpoint; ajusta 'user-info' según tu configuración en urls.py
        self.url = reverse("view user info")

    def test_get_with_hotel_owner(self):
        # Creamos la relación hotel_owner para el usuario
        hotel_owner1 = HotelOwner.objects.create(user=self.user1)
        hotel_owner2 = HotelOwner.objects.create(user=self.user2)

        # Autenticamos al usuario
        # self.client.force_authenticate(user=self.user1)
        self.client.force_authenticate(user=self.user2)

        # Realizamos la petición GET
        response = self.client.get(self.url)

        # Verificamos que la respuesta sea exitosa y contenga el hotel_owner_id correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("hotel_owner", response.data["role"])
        self.assertEqual(response.data["hotel_owner_id"], hotel_owner2.id)
        self.assertEqual(response.data["hotel_owner_id"], 2)

    def test_get_with_customer(self):
        # Creamos la relación customer para el usuario
        customer = Customer.objects.create(user=self.user1)

        # Autenticamos al usuario
        self.client.force_authenticate(user=self.user1)

        # Realizamos la petición GET
        response = self.client.get(self.url)

        # Verificamos que la respuesta sea exitosa y contenga el customer_id correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("hotel_owner", response.data["role"])
        self.assertIn("customer", response.data["role"])
        self.assertNotIn("hotel_owner_id", response.data)
        self.assertEqual(response.data["customer_id"], customer.id)

    def test_get_without_relations(self):
        # No se asocia ninguna relación al usuario

        # Autenticamos al usuario
        self.client.force_authenticate(user=self.user1)

        # Realizamos la petición GET
        response = self.client.get(self.url)

        # Verificamos que la respuesta sea exitosa y que no contenga ni hotel_owner_id ni customer_id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("hotel_owner_id", response.data)
        self.assertNotIn("customer_id", response.data)
