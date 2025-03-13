from django.core.management.base import BaseCommand
from pawtel.room_types.models import PetType, RoomType
from pawtel.hotels.models import Hotel
from faker import Faker
from decimal import Decimal
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = "Seed database with room types"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Room Types..."))

        hotels = list(Hotel.objects.all())
        if not hotels:
            self.stdout.write(self.style.ERROR("No Hotels found. Run seed_hotels first."))
            return

        pet_types = [choice[0] for choice in PetType.choices]

        # Habitaciones deterministas asociadas a hoteles específicos
        self.create_deterministic_room_types()

        self.create_random_room_types(hotels, pet_types, 10)

        self.stdout.write(self.style.SUCCESS("Room Types seeding complete!"))

    def create_deterministic_room_types(self):
        deterministic_rooms = [
            {
                "name": "Suite Ejecutiva",
                "description": "Una suite espaciosa con todas las comodidades para su mascota.",
                "capacity": 2,
                "price_per_night": 250,
                "hotel_name": "Posada Puchero",
                "pet_type": "dog",
            },
            {
                "name": "Habitación Deluxe",
                "description": "Perfecta para mascotas que disfrutan de un trato VIP.",
                "capacity": 3,
                "price_per_night": 350,
                "hotel_name": "Residencia Rancho Lon Lon",
                "pet_type": "cat",
            },
        ]

        for room_data in deterministic_rooms:
            hotel = Hotel.objects.filter(name=room_data["hotel_name"]).first()
            if not hotel:
                self.stdout.write(self.style.ERROR(f"Hotel {room_data['hotel_name']} no encontrado."))
                continue

            if not RoomType.objects.filter(name=room_data["name"], hotel=hotel).exists():
                RoomType.objects.create(
                    name=room_data["name"],
                    description=room_data["description"],
                    capacity=room_data["capacity"],
                    price_per_night=Decimal(room_data["price_per_night"]),
                    pet_type=room_data["pet_type"],
                    hotel=hotel,
                )
                self.stdout.write(self.style.SUCCESS(f"Created Deterministic RoomType: {room_data['name']} ({hotel.name})"))
            else:
                self.stdout.write(self.style.WARNING(f"RoomType {room_data['name']} ya existe en {hotel.name}."))

    def create_random_room_types(self, hotels, pet_types, num_random):
        nombres_tipos_habitacion = [
            "Single", "Doble", "Suite",
            "Habitación Familiar", "Habitación Deluxe", "Habitación Estándar",
            "Suite de Lujo", "Habitación Económica", "Habitación Premium"
        ]

        descripciones_genericas = [
            "Una habitación cómoda y acogedora, diseñada para que tu mascota se sienta como en casa.",
            "Amplia habitación con espacio suficiente para que tu mascota juegue y descanse cómodamente.",
            "Habitación con vistas al jardín, ideal para que tu mascota disfrute de un ambiente relajante.",
            "Diseñada pensando en el bienestar de tu mascota, esta habitación ofrece comodidad y tranquilidad.",
            "Una estancia perfecta para que tu mascota descanse después de un día lleno de actividades.",
        ]

        for _ in range(num_random):
            hotel = random.choice(hotels)
            nombre = random.choice(nombres_tipos_habitacion)
            descripcion = random.choice(descripciones_genericas)

            if RoomType.objects.filter(name=nombre, hotel=hotel).exists():
                nombre = f"{nombre} {fake.word().capitalize()}"

            room_type = RoomType.objects.create(
                name=nombre,
                description=descripcion,
                capacity=fake.random_int(min=1, max=5),
                price_per_night=Decimal(fake.random_int(min=50, max=500)),
                pet_type=random.choice(pet_types),
                hotel=hotel
            )
            self.stdout.write(self.style.SUCCESS(f"Created RoomType: {room_type.name} ({hotel.name})"))
