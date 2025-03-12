from django.core.management.base import BaseCommand
from pawtel.hotels.models import RoomType, Hotel
from faker import Faker
from decimal import Decimal

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with room types"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Room Types..."))
        
        hotels = list(Hotel.objects.all())
        if not hotels:
            self.stdout.write(self.style.ERROR("No Hotels found. Run seed_hotels first."))
            return
        
        pet_types = [choice[0] for choice in RoomType.PetType.choices]
        
        for _ in range(10):  # Crear 10 tipos de habitaciones
            hotel = fake.random_choice(hotels)
            room_type = RoomType.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=300),
                capacity=fake.random_int(min=1, max=5),
                price_per_night=Decimal(fake.random_int(min=50, max=500)),
                pet_type=fake.random_choice(pet_types),
                hotel=hotel
            )
            self.stdout.write(self.style.SUCCESS(f"Created RoomType: {room_type.name} ({hotel.name})"))
        
        self.stdout.write(self.style.SUCCESS("Room Types seeding complete!"))
