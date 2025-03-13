import random

from django.core.management.base import BaseCommand
from faker import Faker
from pawtel.hotels.models import Hotel, HotelOwner

fake = Faker("es_ES")


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
                "city": "Sevilla",
                "description": "Ofrecemos un ambiente tranquilo y seguro para tu perro, con espacios amplios, actividades al aire libre y atención personalizada. Nuestros huéspedes disfrutan de paseos por el campo, juegos y descanso en cómodas instalaciones, garantizando una estancia placentera y relajante.",
                "owner_username": "hotelowner1",
            },
            {
                "name": "Residencia Rancho Lon Lon",
                "address": "Avenida Vía Láctea 64",
                "city": "Córdoba",
                "description": "En nuestro hotel para gatos, cada felino disfruta de habitaciones privadas con vistas panorámicas, juegos interactivos y cuidado especializado. Ideal para aquellos que buscan lo mejor para su mascota, brindando una experiencia cómoda, segura y divertida.",
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
            self.stdout.write(
                self.style.ERROR("No HotelOwners found. Run seed_hotel_owners first.")
            )
            return

        # Lista de ciudades españolas
        ciudades_espanolas = [
            "Madrid",
            "Barcelona",
            "Valencia",
            "Sevilla",
            "Zaragoza",
            "Málaga",
            "Murcia",
            "Palma de Mallorca",
            "Las Palmas de Gran Canaria",
            "Bilbao",
            "Alicante",
            "Córdoba",
            "Valladolid",
            "Vigo",
            "Gijón",
        ]

        # Lista ampliada de nombres de hoteles para mascotas
        nombres_hoteles_mascotas = [
            "Residencia El Rincón del Can", "Alojamiento Patas y Colas", "Hogar de Mascotas Felices",
            "Residencia Peludos", "Refugio Gatuno", "Alojamiento Paraíso Animal",
            "Residencia Amigo Fiel", "Hogar Colmillos", "Refugio Huellas",
            "Alojamiento Mi Mejor Amigo", "Residencia Cachorro Feliz", "Refugio Bigotes",
            "Alojamiento Patitas", "Residencia Colas Alegres", "Hogar Mascota Real",
            "Residencia Paws & Relax", "Alojamiento Happy Tails", "Refugio Furry Friends",
            "Residencia Wagging Tails", "Alojamiento Purrfect Stay", "Refugio Bark Avenue",
            "Residencia Whisker Haven", "Alojamiento Pawsome Place", "Hogar Tail Wagger Inn",
            "Refugio Feline Paradise", "Alojamiento Doggy Retreat", "Residencia Kitty Corner",
            "Refugio Canine Castle", "Alojamiento Meow Manor", "Residencia Puppy Palace",
            "Hogar Whisker Lodge", "Refugio Barkingham Palace", "Alojamiento Paws Inn",
            "Residencia Furry Retreat", "Hogar Tail Haven", "Alojamiento Purr Palace"
        ]

        # Lista de descripciones coherentes para hoteles de mascotas
        descripciones_hoteles_mascotas = [
            "Nuestra residencia ofrece un ambiente cálido y acogedor para tu mascota, con amplias zonas de juego, áreas de descanso confortables y un equipo de cuidadores expertos que garantizan su bienestar. Contamos con un espacio seguro y libre de estrés, ideal para perros y gatos de todas las edades. Además, ofrecemos actividades diarias para mantener a tu mascota activa y feliz durante su estancia.",

            "En nuestro alojamiento de mascotas, nos aseguramos de que tu compañero peludo reciba el mejor cuidado posible. Disponemos de habitaciones individuales y compartidas, con camas cómodas, mantas y juguetes para su entretenimiento. Nuestras instalaciones incluyen patios al aire libre donde pueden correr libremente y una zona de relajación para aquellos que prefieren la tranquilidad.",

            "Si buscas un lugar donde tu mascota se sienta como en casa, nuestra residencia es la opción ideal. Ofrecemos atención personalizada, adaptándonos a las necesidades de cada animal. Contamos con un equipo de veterinarios y cuidadores que supervisan su alimentación, bienestar y estado emocional. Además, organizamos sesiones de socialización y juegos para que hagan nuevos amigos.",

            "Nuestro alojamiento ha sido diseñado para proporcionar la máxima comodidad y seguridad a tu mascota. Contamos con habitaciones amplias, climatización para garantizar su confort en cualquier época del año y un personal altamente capacitado en el cuidado de perros y gatos. También ofrecemos servicios adicionales como peluquería, masajes relajantes y entrenamiento básico.",

            "En nuestra residencia de mascotas, entendemos que separarte de tu compañero puede ser difícil, por eso ofrecemos un servicio de cuidado excepcional que te dará tranquilidad. Nuestras instalaciones incluyen amplias áreas verdes, un parque de juegos con obstáculos, y un equipo de profesionales dedicados a atender las necesidades de cada huésped peludo.",

            "En nuestro alojamiento de lujo para mascotas, cada detalle está pensado para su bienestar. Contamos con suites privadas, áreas de recreación, servicio de alimentación personalizada y atención veterinaria las 24 horas. Además, ofrecemos actividades como paseos diarios, natación y juegos de estimulación mental para que su estancia sea divertida y enriquecedora.",

            "Nuestra residencia es el lugar perfecto para aquellos dueños que buscan un servicio premium para sus mascotas. Aquí recibirán atención exclusiva con instalaciones de primer nivel, menús adaptados a sus necesidades dietéticas y un equipo especializado en comportamiento animal. También ofrecemos servicio de cámaras en vivo para que puedas ver a tu mascota en todo momento.",

            "Deja a tu mascota en las mejores manos mientras viajas o trabajas. Nuestra residencia de mascotas ofrece un ambiente seguro y supervisado, con actividades diarias diseñadas para estimular su mente y cuerpo. Desde paseos hasta sesiones de juegos con otros huéspedes, garantizamos que tu mascota disfrutará cada momento en nuestras instalaciones.",

            "Nuestra residencia canina y felina es mucho más que un simple alojamiento. Aquí brindamos amor, cuidado y atención especializada para que cada mascota se sienta feliz y relajada. Con espacios de descanso cómodos, zonas de socialización y personal altamente calificado, tu mascota vivirá una experiencia única mientras está lejos de casa.",

            "Un espacio diseñado para el máximo confort y diversión de tu mascota. En nuestro alojamiento, cada huésped recibe un trato especial, con rutinas adaptadas a su personalidad y necesidades. Contamos con un jardín para juegos, habitaciones climatizadas y una zona de descanso con música relajante para garantizar su bienestar durante toda su estancia."
        ]


        for _ in range(5):
            owner = random.choice(owners)
            ciudad = random.choice(ciudades_espanolas)
            descripcion = random.choice(descripciones_hoteles_mascotas)
            # Generar un nombre único
            nombre = random.choice(nombres_hoteles_mascotas)
            if Hotel.objects.filter(name=nombre).exists():
                # Si el nombre ya existe, generar uno nuevo con Faker
                nombre = fake.company()
                self.stdout.write(
                    self.style.WARNING(
                        f"Nombre repetido. Generando nuevo nombre: {nombre}"
                    )
                )

            # Generar una dirección ficticia en la ciudad seleccionada
            direccion = f"{fake.street_address()}"

            hotel = Hotel.objects.create(
                name=nombre,
                address=direccion,
                city=ciudad,
                description=descripcion,
                hotel_owner=owner,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created Hotel: {hotel.name} ({hotel.city})")
            )

        self.stdout.write(self.style.SUCCESS("Hotels seeding complete!"))
