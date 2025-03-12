from django.core.management.base import BaseCommand
from pawtel.hotels.models import Hotel, HotelOwner
from faker import Faker
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = "Seed database with hotels"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding Hotels..."))
        
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
        
        # Lista de nombres de hoteles para mascotas
        nombres_hoteles_mascotas = [
            "El Rincón del Can", "Hotel Patas y Colas", "Casa de Mascotas Felices",
            "Hotel Peludos", "Residencia Gatuna", "Hotel Paraíso Animal",
            "Hotel Amigo Fiel", "Hotel Colmillos", "Hotel Huellas",
            "Hotel Mi Mejor Amigo", "Hotel Cachorro Feliz", "Hotel Bigotes",
            "Hotel Patitas", "Hotel Colas Alegres", "Hotel Mascota Real"
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
        
        for _ in range(5):
            owner = random.choice(owners)
            ciudad = random.choice(ciudades_espanolas)
            nombre = random.choice(nombres_hoteles_mascotas)
            descripcion = random.choice(descripciones_hoteles_mascotas)
            
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
        
        self.stdout.write(self.style.SUCCESS("Hotels seeding complete!"))