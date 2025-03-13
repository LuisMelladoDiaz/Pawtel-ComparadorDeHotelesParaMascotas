from django.core.management.base import BaseCommand
from pawtel.hotels.models import Hotel
from pawtel.room_types.models import PetType, RoomType


class Command(BaseCommand):
    help = "Crea algunos tipos de habitaciones de prueba"

    def handle(self, *args, **kwargs):
        # Eliminar todas las habitaciones antes de crear nuevas
        # RoomType.objects.all().delete()
        # self.stdout.write(self.style.WARNING('Todos los tipos de habitaciones han sido eliminados.'))

        # Verificar si existen hoteles
        hotels = Hotel.objects.all()
        if not hotels.exists():
            self.stdout.write(
                self.style.ERROR(
                    "No hay hoteles en la base de datos. Ejecuta el seeder de hoteles primero."
                )
            )
            return

        room_types = [
            {
                "name": "Habitación Estándar",
                "description": "Una habitación cómoda para perros.",
                "capacity": 2,
                "price_per_night": 30.00,
                "pet_type": PetType.DOG,
            },
            {
                "name": "Suite de Lujo",
                "description": "Una suite amplia y lujosa para gatos.",
                "capacity": 1,
                "price_per_night": 50.00,
                "pet_type": PetType.CAT,
            },
            {
                "name": "Habitación Compartida",
                "description": "Un espacio compartido ideal para aves.",
                "capacity": 4,
                "price_per_night": 20.00,
                "pet_type": PetType.BIRD,
            },
            {
                "name": "Habitación Mixta",
                "description": "Perfecta para mascotas de diferentes tipos.",
                "capacity": 3,
                "price_per_night": 35.00,
                "pet_type": PetType.MIXED,
            },
        ]

        for hotel in hotels:
            for room_data in room_types:
                room = RoomType.objects.create(hotel=hotel, **room_data)
                self.stdout.write(
                    self.style.SUCCESS(f"Habitación {room.name} creada en {hotel.name}")
                )
