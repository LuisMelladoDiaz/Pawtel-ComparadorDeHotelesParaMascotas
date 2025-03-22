import io
import random

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management.base import BaseCommand
from faker import Faker
from pawtel.hotels.models import Hotel, HotelImage
from PIL import Image

fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Seed hotel images"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding hotel images..."))
        hotels = Hotel.objects.all()

        if not hotels:
            self.stdout.write(
                self.style.ERROR(
                    "No hotels found. Please run the seed for hotels first."
                )
            )
            return

        self.create_hotel_images(hotels, 5)
        self.stdout.write(self.style.SUCCESS("Hotel images seeding complete!"))

    def create_hotel_images(self, hotels, num_images_per_hotel):
        for hotel in hotels:
            # Primero crea la imagen de portada (cover image)
            cover_image = self.generate_image(is_cover=True)
            HotelImage.objects.create(hotel=hotel, image=cover_image, is_cover=True)
            self.stdout.write(
                self.style.SUCCESS(f"Created cover image for Hotel: {hotel.name}")
            )

            # Luego crea las imágenes adicionales (no cover)
            for _ in range(num_images_per_hotel - 1):
                image = self.generate_image(is_cover=False)
                HotelImage.objects.create(hotel=hotel, image=image, is_cover=False)
                self.stdout.write(
                    self.style.SUCCESS(f"Created image for Hotel: {hotel.name}")
                )

    def generate_image(self, is_cover=False):
        img = Image.new(
            "RGB",
            (200, 200),
            color=(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ),
        )
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)
        image_file = InMemoryUploadedFile(
            img_byte_arr,
            None,
            "hotel_image.jpg",
            "image/jpeg",
            img_byte_arr.tell(),
            None,
        )
        return image_file
