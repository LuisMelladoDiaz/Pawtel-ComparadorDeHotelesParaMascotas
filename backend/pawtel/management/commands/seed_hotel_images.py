import os
import random

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from pawtel.hotels.models import Hotel, HotelImage


class Command(BaseCommand):
    help = "Seed hotel images"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Hotel Images..."))

        image_dir = os.path.join(settings.BASE_DIR, "pawtel", "images_hotel")

        if not os.path.exists(image_dir):
            self.stdout.write(
                self.style.ERROR(f"No se encontró la carpeta {image_dir}")
            )
            return

        image_files = os.listdir(image_dir)

        if not image_files:
            self.stdout.write(self.style.WARNING("No hay imágenes para cargar."))
            return

        hotels = Hotel.objects.all()
        if not hotels.exists():
            self.stdout.write(
                self.style.ERROR("No hay hoteles registrados en la base de datos.")
            )
            return

        image_files_copy = image_files.copy()

        for hotel in hotels:
            if image_files_copy:
                cover_image_file = random.choice(image_files_copy)
                image_files_copy.remove(cover_image_file)
            else:
                cover_image_file = random.choice(image_files)

            self.create_hotel_image(hotel, cover_image_file, is_cover=True)

            remaining_images = list(set(image_files) - {cover_image_file})
            random.shuffle(remaining_images)

            for image_file in remaining_images[:4]:
                self.create_hotel_image(hotel, image_file, is_cover=False)

        self.stdout.write(self.style.SUCCESS("Hotel Images seeding complete!"))

    def create_hotel_image(self, hotel, image_file, is_cover):
        image_dir = os.path.join(settings.BASE_DIR, "pawtel", "images_hotel")
        image_path = os.path.join(image_dir, image_file)

        with open(image_path, "rb") as f:
            hotel_image = HotelImage(
                hotel=hotel, image=File(f, name=image_file), is_cover=is_cover
            )
            hotel_image.save()

        label = "cover image" if is_cover else "image"
        self.stdout.write(self.style.SUCCESS(f"Created {label} for {hotel.name}"))
