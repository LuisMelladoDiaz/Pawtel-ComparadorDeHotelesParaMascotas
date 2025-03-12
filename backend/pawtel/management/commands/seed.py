from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room
from pawtel.hotels.models import Hotel
from pawtel.app_users.models import AppUser
from pawtel.hotels.models import HotelOwner

class Command(BaseCommand):
    help = "Seed the entire database with test data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clean']:
            confirm = input("Are you sure you want to delete all existing data before seeding? (yes/no): ")
            if confirm.lower() == 'yes':
                self.stdout.write(self.style.WARNING("Deleting existing data..."))
                Room.objects.all().delete()
                RoomType.objects.all().delete()
                Hotel.objects.all().delete()
                HotelOwner.objects.all().delete()
                AppUser.objects.all().delete()
                self.stdout.write(self.style.SUCCESS("All relevant data deleted."))
            else:
                self.stdout.write(self.style.WARNING("Skipping data deletion."))

        self.stdout.write(self.style.SUCCESS("Seeding database..."))

        try:
            call_command("seed_hotel_owners")
            call_command("seed_hotels")
            call_command("seed_room_types")
            call_command("seed_rooms")
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"Error while seeding: {e}"))
            return

        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
