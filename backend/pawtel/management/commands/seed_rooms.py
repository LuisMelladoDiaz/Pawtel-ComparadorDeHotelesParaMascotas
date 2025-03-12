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
        
        # Letras posibles para el nombre de la habitación
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        for _ in range(20):  # Crear 20 habitaciones
            room_type = random.choice(room_types)
            letra = random.choice(letras)
            numero = fake.random_int(min=10, max=99)
            nombre_habitacion = f"{letra}{numero}"
            
            room = Room.objects.create(
                name=nombre_habitacion,
                room_type=room_type
            )
            self.stdout.write(self.style.SUCCESS(f"Created Room: {room.name} ({room_type.name})"))
        
        self.stdout.write(self.style.SUCCESS("Rooms seeding complete!"))