from django.core.management.base import BaseCommand
from faker import Faker
import random
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room

fake = Faker('es_ES')


class Command(BaseCommand):
    help = "Seed database with rooms"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Rooms..."))

        room_types = list(RoomType.objects.all())
        if not room_types:
            self.stdout.write(self.style.ERROR("No RoomTypes found. Run seed_room_types first."))
            return

        # Crear habitaciones deterministas
        self.create_deterministic_rooms()

        self.create_random_rooms(room_types, 20)

        self.stdout.write(self.style.SUCCESS("Rooms seeding complete!"))

    def create_deterministic_rooms(self):
        deterministic_rooms = [
            {"name": "A10", "room_type_name": "Suite Ejecutiva"},
            {"name": "B20", "room_type_name": "Habitación Deluxe"},
        ]

        for room_data in deterministic_rooms:
            room_type = RoomType.objects.filter(name=room_data["room_type_name"]).first()
            if not room_type:
                self.stdout.write(self.style.ERROR(f"RoomType {room_data['room_type_name']} no encontrado."))
                continue

            if not Room.objects.filter(name=room_data["name"], room_type=room_type).exists():
                Room.objects.create(
                    name=room_data["name"],
                    room_type=room_type
                )
                self.stdout.write(self.style.SUCCESS(f"Created Deterministic Room: {room_data['name']} ({room_type.name})"))
            else:
                self.stdout.write(self.style.WARNING(f"Room {room_data['name']} ya existe para {room_type.name}."))

    def create_random_rooms(self, room_types, num_random):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for _ in range(num_random):
            room_type = random.choice(room_types)
            nombre_habitacion = self.generate_unique_room_name()

            Room.objects.create(
                name=nombre_habitacion,
                room_type=room_type
            )
            self.stdout.write(self.style.SUCCESS(f"Created Room: {nombre_habitacion} ({room_type.name})"))

    def generate_unique_room_name(self):
        """
        Genera un nombre único para la habitación en formato 'Letra + Número',
        asegurándose de que no exista en la base de datos.
        """
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        while True:
            letra = random.choice(letras)
            numero = fake.random_int(min=10, max=99)
            nombre_habitacion = f"{letra}{numero}"

            if not Room.objects.filter(name=nombre_habitacion).exists():
                return nombre_habitacion
