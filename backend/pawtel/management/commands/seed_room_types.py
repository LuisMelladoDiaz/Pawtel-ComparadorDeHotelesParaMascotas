import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType

fake = Faker("es_ES")
Faker.seed(6)
random.seed(6)


class Command(BaseCommand):
    help = "Seed database with room types"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Room Types..."))

        hotels = list(Hotel.objects.all())
        if not hotels:
            self.stdout.write(
                self.style.ERROR("No Hotels found. Run seed_hotels first.")
            )
            return

        pet_types = [choice[0] for choice in PetType.choices]

        # Lista de nombres coherentes para tipos de habitación
        nombres_tipos_habitacion = [
            "Single",
            "Doble",
            "Suite",
            "Habitación Familiar",
            "Habitación Deluxe",
            "Habitación Estándar",
            "Suite de Lujo",
            "Habitación Económica",
            "Habitación Premium",
        ]

        # Lista de descripciones genéricas que encajan con cualquier tipo de habitación
        descripciones_genericas = [
            "Una habitación cómoda y acogedora, diseñada para que tu mascota se sienta como en casa.",
            "Amplia habitación con espacio suficiente para que tu mascota juegue y descanse cómodamente.",
            "Habitación con vistas al jardín, ideal para que tu mascota disfrute de un ambiente relajante.",
            "Diseñada pensando en el bienestar de tu mascota, esta habitación ofrece comodidad y tranquilidad.",
            "Una estancia perfecta para que tu mascota descanse después de un día lleno de actividades.",
            "Habitación con camas suaves y áreas de descanso, perfecta para mascotas de todos los tamaños.",
            "Un espacio seguro y confortable, donde tu mascota recibirá todo el cuidado que necesita.",
            "Habitación con juguetes y áreas de entretenimiento para que tu mascota nunca se aburra.",
            "Diseño moderno y funcional, pensado para ofrecer el máximo confort a tu mascota.",
            "Habitación con servicio personalizado, asegurando que tu mascota tenga una estancia inolvidable.",
        ]

        for _ in range(150):  # Crear 10 tipos de habitaciones
            hotel = random.choice(hotels)
            nombre = random.choice(nombres_tipos_habitacion)
            descripcion = random.choice(descripciones_genericas)

            room_type = RoomType.objects.create(
                name=nombre,
                description=descripcion,
                capacity=fake.random_int(min=1, max=50),
                num_rooms=fake.random_int(min=1, max=50),
                price_per_night=Decimal(fake.random_int(min=10, max=100)),
                pet_type=random.choice(pet_types),
                hotel=hotel,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created RoomType: {room_type.name} ({hotel.name})")
            )

        self.stdout.write(self.style.SUCCESS("Room Types seeding complete!"))
