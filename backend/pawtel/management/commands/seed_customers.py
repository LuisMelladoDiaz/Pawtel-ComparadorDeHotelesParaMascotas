from django.core.management.base import BaseCommand
from faker import Faker
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer

fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Seed database with customers"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Customers..."))

        # Crear usuarios deterministas solo si no existen
        self.create_deterministic_users()

        self.create_random_customers(10)

        self.stdout.write(self.style.SUCCESS("Customers seeding complete!"))

    def create_deterministic_users(self):
        username1 = "customer1"
        email1 = "example3@example.com"
        phone1 = "+34600000002"

        if not AppUser.objects.filter(username=username1).exists():
            user1 = AppUser.objects.create_user(
                username=username1,
                email=email1,
                phone=phone1,
                password="password123",
            )
            Customer.objects.create(user=user1)
            self.stdout.write(self.style.SUCCESS(f"Created Customer: {username1}"))

        username2 = "customer2"
        email2 = "example4@example.com"
        phone2 = "+34600000003"

        if not AppUser.objects.filter(username=username2).exists():
            user2 = AppUser.objects.create_user(
                username=username2,
                email=email2,
                phone=phone2,
                password="password123",
            )
            Customer.objects.create(user=user2)
            self.stdout.write(self.style.SUCCESS(f"Created Customer: {username2}"))

    def create_random_customers(self, num_random):
        for _ in range(num_random):
            username = fake.user_name()
            email = fake.unique.email()
            phone = f"+34{fake.random_int(min=600000000, max=699999999)}"

            user = AppUser.objects.create_user(
                username=username, email=email, phone=phone, password="password123"
            )

            Customer.objects.create(user=user)

            self.stdout.write(
                self.style.SUCCESS(f"Created Customer: {username} ({email})")
            )
