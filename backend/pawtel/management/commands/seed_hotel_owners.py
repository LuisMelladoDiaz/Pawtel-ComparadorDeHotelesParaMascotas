from django.core.management.base import BaseCommand
from faker import Faker
from pawtel.app_users.models import AppUser
from pawtel.hotels.models import HotelOwner

fake = Faker('es_ES')


class Command(BaseCommand):
    help = "Seed database with hotel owners"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Hotel Owners..."))

        # Crear usuarios deterministas solo si no existen
        self.create_deterministic_users()

        self.create_random_hotel_owners(10)

        self.stdout.write(self.style.SUCCESS("Hotel Owners seeding complete!"))

    def create_deterministic_users(self):
        username1 = "hotelowner1"
        email1 = "example1@example.com"
        phone1 = "+34600000000"

        if not AppUser.objects.filter(username=username1).exists():
            user1 = AppUser.objects.create_user(
                username=username1,
                email=email1,
                phone=phone1,
                password="password123",
            )
            HotelOwner.objects.create(user=user1)
            self.stdout.write(self.style.SUCCESS(f"Created HotelOwner: {username1}"))

        username2 = "hotelowner2"
        email2 = "example2@example.com"
        phone2 = "+34600000001"

        if not AppUser.objects.filter(username=username2).exists():
            user2 = AppUser.objects.create_user(
                username=username2,
                email=email2,
                phone=phone2,
                password="password123",
            )
            HotelOwner.objects.create(user=user2)
            self.stdout.write(self.style.SUCCESS(f"Created HotelOwner: {username2}"))

    def create_random_hotel_owners(self, num_random):
        for _ in range(num_random):  # Crear 10 dueños de hoteles con datos aleatorios
            username = fake.user_name()
            email = fake.unique.email()
            phone = f"+34{fake.random_int(min=600000000, max=699999999)}"

            user = AppUser.objects.create_user(
                username=username, email=email, phone=phone, password="password123"
            )

            HotelOwner.objects.create(user=user)

            self.stdout.write(
                self.style.SUCCESS(f"Created HotelOwner: {username} ({email})")
            )
