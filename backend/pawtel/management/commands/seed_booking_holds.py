import random
from datetime import date

from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from faker import Faker
from pawtel.booking_holds.models import BookingHold
from pawtel.customers.models import Customer
from pawtel.room_types.models import RoomType

fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Seed database with booking holds"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Booking Holds..."))

        self.create_deterministic_booking_holds()
        self.create_random_booking_holds(5)

        self.stdout.write(self.style.SUCCESS("Booking Holds seeding complete!"))

    def create_deterministic_booking_holds(self):
        deterministic_holds = [
            {
                "customer_username": "customer1",
                "room_type_name": "Single",
                "booking_start_date": date.today() + timedelta(days=2),
                "booking_end_date": date.today() + timedelta(days=5),
            },
            {
                "customer_username": "customer2",
                "room_type_name": "Suite",
                "booking_start_date": date.today() + timedelta(days=3),
                "booking_end_date": date.today() + timedelta(days=7),
            },
        ]

        for hold_data in deterministic_holds:
            customer = Customer.objects.filter(
                user__username=hold_data["customer_username"]
            ).first()
            if not customer:
                self.stdout.write(
                    self.style.ERROR(
                        f"Customer {hold_data['customer_username']} no encontrado."
                    )
                )
                continue

            room_type = RoomType.objects.filter(
                name=hold_data["room_type_name"]
            ).first()
            if not room_type:
                self.stdout.write(
                    self.style.ERROR(
                        f"RoomType {hold_data['room_type_name']} no encontrado."
                    )
                )
                continue

            if not BookingHold.objects.filter(
                customer=customer,
                room_type=room_type,
                booking_start_date=hold_data["booking_start_date"],
                booking_end_date=hold_data["booking_end_date"],
            ).exists():
                BookingHold.objects.create(
                    customer=customer,
                    room_type=room_type,
                    booking_start_date=hold_data["booking_start_date"],
                    booking_end_date=hold_data["booking_end_date"],
                    hold_expires_at=now() + timedelta(minutes=10),
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created deterministic BookingHold for {customer} with room type {room_type.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"BookingHold for {customer} with room type {room_type.name} ya existe."
                    )
                )

    def create_random_booking_holds(self, num_random):
        customers = list(Customer.objects.all())
        room_types = list(RoomType.objects.all())

        if not customers:
            self.stdout.write(
                self.style.ERROR(
                    "No se encontraron Customers. Ejecuta el seed de Customers primero."
                )
            )
            return

        if not room_types:
            self.stdout.write(
                self.style.ERROR(
                    "No se encontraron RoomTypes. Ejecuta el seed de RoomTypes primero."
                )
            )
            return

        for _ in range(num_random):
            customer = random.choice(customers)
            room_type = random.choice(room_types)
            start_offset = random.randint(2, 10)
            end_offset = random.randint(start_offset + 1, start_offset + 5)
            booking_start = date.today() + timedelta(days=start_offset)
            booking_end = date.today() + timedelta(days=end_offset)

            if not BookingHold.objects.filter(
                customer=customer,
                room_type=room_type,
                booking_start_date=booking_start,
                booking_end_date=booking_end,
            ).exists():
                BookingHold.objects.create(
                    customer=customer,
                    room_type=room_type,
                    booking_start_date=booking_start,
                    booking_end_date=booking_end,
                    hold_expires_at=now() + timedelta(minutes=10),
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created BookingHold for {customer} and room type {room_type.name} ({booking_start} - {booking_end})"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"BookingHold for {customer} and room type {room_type.name} ({booking_start} - {booking_end}) ya existe."
                    )
                )

        self.stdout.write(self.style.SUCCESS("Random Booking Holds seeding complete!"))
