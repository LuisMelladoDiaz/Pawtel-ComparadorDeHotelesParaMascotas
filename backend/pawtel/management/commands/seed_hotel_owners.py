from django.core.management.base import BaseCommand
from pawtel.app_users.models import AppUser
from pawtel.hotels.models import HotelOwner
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with hotel owners"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Hotel Owners..."))
        
        for _ in range(10):  # Crear 10 dueños de hoteles con datos aleatorios
            username = fake.user_name()
            email = fake.unique.email()
            phone = f"+34{fake.random_int(min=600000000, max=699999999)}"
            
            user = AppUser.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                password="password123"
            )
            
            HotelOwner.objects.create(user=user)
            
            self.stdout.write(self.style.SUCCESS(f"Created HotelOwner: {username} ({email})"))
        
        self.stdout.write(self.style.SUCCESS("Hotel Owners seeding complete!"))
