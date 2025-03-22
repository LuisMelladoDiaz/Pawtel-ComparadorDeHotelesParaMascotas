from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from pawtel.app_users.models import AppUser
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import RoomType
from rest_framework import status
from rest_framework.test import APIClient

class HotelViewSetTestCase2(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.app_user3 = AppUser.objects.create_user(
            username="hotel_owner2",
            first_name="Johnttt",
            last_name="Dotte",
            email="owner32@example.com",
            phone="+34987654444",
            password="password456",
        )
        self.client.force_authenticate(user=self.app_user3)
        self.hotel_owner4 = HotelOwner.objects.create(user_id=self.app_user3.id)

        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            address="123 Street",
            city="Madrid",
            description="Hotel de prueba",
            hotel_owner=self.hotel_owner4,
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Suite",
            description="Luxury suite",
            capacity=1,
            num_rooms=1,
            price_per_night=150.00,
            pet_type="DOG",
        )

        self.app_user2 = AppUser.objects.create_user(
            username="customer_user",
            first_name="Pepita",
            last_name="Flores",
            email="customer43@example.com",
            phone="+34987654322",
            password="password923",
        )

        self.customer = Customer.objects.create(user_id=self.app_user2.id)

        # Se crea una reserva que ocupa parte del rango
        self.booking1 = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=6),
            end_date=date.today() + timedelta(days=8),
            total_price=450.00,
        )
        # Otra reserva en otro intervalo (no se solapa con el primer booking)
        self.booking2 = Booking.objects.create(
            customer=self.customer,
            room_type=self.room_type,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            total_price=300.00,
        )

class TestNuevasRutasHotel(HotelViewSetTestCase2):
    def test_available_hotels_con_room_type_disponible(self):
        """
        Se debe retornar el hotel cuando, en el intervalo dado, 
        al menos uno de sus room types se encuentre disponible.
        Se selecciona un rango que NO se solape con ninguna reserva.
        """
        # Escogemos un rango posterior a booking1 y anterior a booking2
        start_date = date.today() + timedelta(days=2)
        end_date = start_date + timedelta(days=2)
        
        # Se asume que la ruta fue registrada con el nombre 'hotel-available-hotels'
        url = reverse("hotel-available_hotels")
        response = self.client.get(url, {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], "Madrid")

    def test_available_room_types_con_disponibilidad(self):
        """
        Dado un hotel, se deben retornar los room types disponibles en el rango seleccionado.
        Se escoge un rango sin reservas.
        """
        start_date = date.today() + timedelta(days=4)
        end_date = start_date + timedelta(days=1)
        
        # Se asume que la ruta fue registrada con el nombre 'hotel-available-room-types'
        url = reverse("hotel-available_room_types", kwargs={"pk": self.hotel.id})
        response = self.client.get(url, {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Se espera que el room type del hotel esté disponible y se retorne
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.room_type.id)

    def test_available_hotels_sin_room_type_disponible(self):
        """
        Se debe retornar una lista vacía si en el rango solicitado el room type está ocupado.
        """
        start_date = date.today() + timedelta(days=6)  # Exactamente cuando booking1 está activa
        end_date = date.today() + timedelta(days=8)  # Coincide con booking1 y booking2
        
        url = reverse("hotel-available_hotels")
        response = self.client.get(url, {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Ahora sí debería fallar si la lógica está mal

    def test_available_room_types_sin_disponibilidad(self):
        """
        Para un hotel dado, se debe retornar una lista vacía de room types 
        si en el rango solicitado el room type está ocupado.
        """
        start_date = date.today() + timedelta(days=4)  # Durante booking1
        end_date = date.today() + timedelta(days=7)  # Durante booking2 también
        
        url = reverse("hotel-available_room_types", kwargs={"pk": self.hotel.id})
        response = self.client.get(url, {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Esto debería pasar si la lógica está bien
