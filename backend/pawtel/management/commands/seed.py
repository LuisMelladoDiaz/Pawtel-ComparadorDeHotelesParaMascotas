from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from pawtel.app_users.models import AppUser
from pawtel.customers.models import Customer
from pawtel.hotels.models import Hotel, HotelOwner
from pawtel.room_types.models import RoomType


class Command(BaseCommand):
    help = "Seed the entire database with test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Delete existing data before seeding",
        )
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Do not prompt the user for input of any kind",
        )

    def handle(self, *args, **options):
        if options["clean"]:
            confirm = (
                "yes"
                if options["noinput"]
                else input(
                    "Are you sure you want to delete all existing data? (yes/no): "
                )
            )
            if confirm.lower() == "yes":
                self.stdout.write(self.style.WARNING("Deleting existing data..."))
                RoomType.objects.all().delete()
                Hotel.objects.all().delete()
                HotelOwner.objects.all().delete()
                Customer.objects.all().delete()
                AppUser.objects.all().delete()
                self.stdout.write(self.style.SUCCESS("All relevant data deleted."))
            else:
                self.stdout.write(self.style.WARNING("Skipping data deletion."))

        self.stdout.write(self.style.SUCCESS("Seeding database..."))

        try:
            call_command("seed_hotel_owners")
            call_command("seed_customers")
            call_command("seed_hotels")
            call_command("seed_room_types")
            call_command("seed_hotel_images")
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"Error while seeding: {e}"))
            return

        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
