from django.core.management.base import BaseCommand
from pawtel.hotels.models import Hotel, HotelOwner
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with hotels"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Hotels..."))
        
        owners = list(HotelOwner.objects.all())
        if not owners:
            self.stdout.write(self.style.ERROR("No HotelOwners found. Run seed_hotel_owners first."))
            return
        
        for _ in range(5):  # Crear 5 hoteles
            owner = fake.random_choice(owners)
            hotel = Hotel.objects.create(
                name=fake.company(),
                address=fake.address(),
                city=fake.city(),
                description=fake.text(max_nb_chars=300),
                hotel_owner=owner
            )
            self.stdout.write(self.style.SUCCESS(f"Created Hotel: {hotel.name} ({hotel.city})"))
        
        self.stdout.write(self.style.SUCCESS("Hotels seeding complete!"))
