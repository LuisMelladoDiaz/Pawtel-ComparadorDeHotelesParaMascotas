from django.core.management.base import BaseCommand
from faker import Faker
from pawtel.app_admins.models import App_Admin
from pawtel.app_users.models import AppUser

fake = Faker("es_ES")
Faker.seed(1)



class Command(BaseCommand):
    help = "Seed database with admins"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Admins..."))

        # Crear admins deterministas solo si no existen
        self.create_deterministic_admins()

        self.stdout.write(self.style.SUCCESS("Admins seeding complete!"))

    def create_deterministic_admins(self):
        admins_data = [
            {
                "username": "admin1",
                "email": "admin1@example.com",
                "phone": "+34600000010",
            },
            {
                "username": "admin2",
                "email": "admin2@example.com",
                "phone": "+34600000011",
            },
        ]

        for admin_data in admins_data:
            if not AppUser.objects.filter(username=admin_data["username"]).exists():
                user = AppUser.objects.create_user(
                    username=admin_data["username"],
                    email=admin_data["email"],
                    phone=admin_data["phone"],
                    password="password123",
                )
                App_Admin.objects.create(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f"Created Admin: {admin_data['username']}")
                )
