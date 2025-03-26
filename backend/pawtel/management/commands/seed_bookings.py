from datetime import date, timedelta
from random import choice, randint

from django.core.management.base import BaseCommand
from faker import Faker
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.room_types.models import RoomType

fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Seed database with bookings"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Bookings..."))

        self.create_deterministic_bookings()
        self.create_random_bookings(10)

        self.stdout.write(self.style.SUCCESS("Bookings seeding complete!"))

    def create_deterministic_bookings(self):
        customer = Customer.objects.first()
        room_type = RoomType.objects.first()

        if customer and room_type:
            start_date = date.today() + timedelta(days=5)
            end_date = start_date + timedelta(days=randint(1, 7))
            total_price = room_type.price_per_night * (end_date - start_date).days

            Booking.objects.create(
                customer=customer,
                room_type=room_type,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created deterministic booking for {customer}")
            )

    def create_random_bookings(self, num_random):
        customers = list(Customer.objects.all())
        room_types = list(RoomType.objects.all())

        if not customers or not room_types:
            self.stdout.write(
                self.style.ERROR(
                    "No customers or room types found. Cannot create bookings."
                )
            )
            return

        for _ in range(num_random):
            customer = choice(customers)
            room_type = choice(room_types)

            start_date = date.today() + timedelta(days=randint(1, 30))
            end_date = start_date + timedelta(days=randint(1, 7))
            total_price = room_type.price_per_night * (end_date - start_date).days

            Booking.objects.create(
                customer=customer,
                room_type=room_type,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
            )

            self.stdout.write(
                self.style.SUCCESS(f"Created Booking for {customer.user.username}")
            )
