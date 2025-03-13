from django.core.management.base import BaseCommand
from django.core.management import call_command
from faker import Faker
import random
from pawtel.hotels.models import Hotel, HotelOwner

fake = Faker('es_ES')

class Command(BaseCommand):
    help = "Seed database with hotels"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Hotels..."))

        # Crear hoteles deterministas asociados a hotelowner1 y hotelowner2
        self.create_deterministic_hotels()

        self.create_random_hotels(5)

        self.stdout.write(self.style.SUCCESS("Hotels seeding complete!"))

    def create_deterministic_hotels(self):
        # Hoteles deterministas
        deterministic_hotels = [
            {
                "name": "Posada Puchero",
                "address": "Calle Este 8",
                "city": "Términa",
                "description": "Un lugar donde tu mascota se sentirá como en casa.",
                "owner_username": "hotelowner1",
            },
            {
                "name": "Residencia Rancho Lon Lon",
                "address": "Avenida Vía Láctea 64",
                "city": "Hyrule",
                "description": "Ofrecemos el mejor cuidado para tu mascota.",
                "owner_username": "hotelowner2",
            },
        ]

        for hotel_data in deterministic_hotels:
            owner = HotelOwner.objects.filter(user__username=hotel_data["owner_username"]).first()
            if not owner:
                self.stdout.write(
                    self.style.ERROR(f"HotelOwner {hotel_data['owner_username']} no encontrado.")
                )
                continue

            if not Hotel.objects.filter(name=hotel_data["name"]).exists():
                Hotel.objects.create(
                    name=hotel_data["name"],
                    address=hotel_data["address"],
                    city=hotel_data["city"],
                    description=hotel_data["description"],
                    hotel_owner=owner,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Created Deterministic Hotel: {hotel_data['name']}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Hotel {hotel_data['name']} ya existe.")
                )

    def create_random_hotels(self, num_random):
        owners = list(HotelOwner.objects.all())
        if not owners:
            self.stdout.write(self.style.ERROR("No HotelOwners found. Run seed_hotel_owners first."))
            return

        # Lista de ciudades españolas
        ciudades_espanolas = [
            "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza",
            "Málaga", "Murcia", "Palma de Mallorca", "Las Palmas de Gran Canaria",
            "Bilbao", "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón"
        ]

        # Lista ampliada de nombres de hoteles para mascotas
        nombres_hoteles_mascotas = [
            "El Rincón del Can", "Hotel Patas y Colas", "Casa de Mascotas Felices",
            "Hotel Peludos", "Residencia Gatuna", "Hotel Paraíso Animal",
            "Hotel Amigo Fiel", "Hotel Colmillos", "Hotel Huellas",
            "Hotel Mi Mejor Amigo", "Hotel Cachorro Feliz", "Hotel Bigotes",
            "Hotel Patitas", "Hotel Colas Alegres", "Hotel Mascota Real",
            "Hotel Paws & Relax", "Hotel Happy Tails", "Hotel Furry Friends",
            "Hotel Wagging Tails", "Hotel Purrfect Stay", "Hotel Bark Avenue",
            "Hotel Whisker Haven", "Hotel Pawsome Place", "Hotel Tail Wagger Inn",
            "Hotel Feline Paradise", "Hotel Doggy Retreat", "Hotel Kitty Corner",
            "Hotel Canine Castle", "Hotel Meow Manor", "Hotel Puppy Palace",
            "Hotel Whisker Lodge", "Hotel Barkingham Palace", "Hotel Paws Inn",
            "Hotel Furry Retreat", "Hotel Tail Haven", "Hotel Purr Palace"
        ]

        # Lista de descripciones coherentes para hoteles de mascotas
        descripciones_hoteles_mascotas = [
            "Un lugar donde tu mascota se sentirá como en casa. Con amplios espacios y cuidados personalizados.",
            "Ofrecemos el mejor cuidado para tu mascota, con actividades recreativas y atención veterinaria.",
            "Nuestro hotel está diseñado para que tu mascota disfrute de unas vacaciones inolvidables.",
            "Cuidamos de tu mascota como si fuera nuestra. Con instalaciones de lujo y personal especializado.",
            "Un espacio seguro y divertido para tu mascota. Con áreas de juego y descanso.",
            "Tu mascota merece lo mejor. En nuestro hotel, recibirá atención personalizada y mucho cariño.",
            "Ofrecemos un ambiente familiar donde tu mascota se sentirá cómoda y feliz.",
            "Nuestro equipo está dedicado a proporcionar el mejor cuidado y atención a tu mascota.",
            "Un lugar donde tu mascota puede relajarse y disfrutar de su estancia con comodidad y seguridad.",
            "En nuestro hotel, tu mascota es nuestra prioridad. Ofrecemos servicios de calidad y mucho amor."
        ]

        for _ in range(num_random):
            owner = random.choice(owners)
            ciudad = random.choice(ciudades_espanolas)
            descripcion = random.choice(descripciones_hoteles_mascotas)

            # Generar un nombre único
            nombre = random.choice(nombres_hoteles_mascotas)
            if Hotel.objects.filter(name=nombre).exists():
                # Si el nombre ya existe, generar uno nuevo con Faker
                nombre = fake.company()
                self.stdout.write(self.style.WARNING(f"Nombre repetido. Generando nuevo nombre: {nombre}"))

            # Generar una dirección ficticia en la ciudad seleccionada
            direccion = f"{fake.street_address()}"

            hotel = Hotel.objects.create(
                name=nombre,
                address=direccion,
                city=ciudad,
                description=descripcion,
                hotel_owner=owner
            )
            self.stdout.write(self.style.SUCCESS(f"Created Hotel: {hotel.name} ({hotel.city})"))
