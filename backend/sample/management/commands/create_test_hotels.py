from django.core.management.base import BaseCommand
from pawtel.hotel_owners.services import HotelOwner
from pawtel.hotels.models import Hotel

class Command(BaseCommand):
    help = 'Crea algunos hoteles de prueba'

    def handle(self, *args, **kwargs):
        # Eliminar todas los hoteles antes de crear nuevos
        Hotel.objects.all().delete()
        self.stdout.write(self.style.WARNING('Todos los hoteles han sido eliminados.'))

        # Verificar si ya existen propietarios de hoteles
        hotel_owner = HotelOwner.objects.first()

        # Crear algunos hoteles de prueba
        hotels = [
            {
                'name': 'Residencia Canina Sol',
                'address': 'Calle de Alcalá 45',
                'city': 'Madrid',
                'description': 'Un espacio seguro y cómodo para perros en el centro de Madrid, con amplias zonas de recreo.',
                'hotel_owner': hotel_owner,
            },
            {
                'name': 'Dog Resort Luna',
                'address': 'Passeig de Gràcia 22',
                'city': 'Barcelona',
                'description': 'Una residencia de lujo con vistas al mar, ideal para el descanso y la diversión de tu mascota.',
                'hotel_owner': hotel_owner,
            },
            {
                'name': 'Hogar Canino Estrella',
                'address': 'Avenida del Puerto 15',
                'city': 'Valencia',
                'description': 'Un centro de alojamiento premium con veterinario 24h y parque de juegos para perros.',
                'hotel_owner': hotel_owner,
            },
            {
                'name': 'Parque Canino Giralda',
                'address': 'Calle San Fernando 30',
                'city': 'Sevilla',
                'description': 'Residencia moderna con zonas verdes y servicio de entrenamiento personalizado para perros.',
                'hotel_owner': hotel_owner,
            },
            {
                'name': 'BilboDog Retreat',
                'address': 'Gran Vía de Don Diego López de Haro 12',
                'city': 'Bilbao',
                'description': 'Un hogar temporal ideal para perros, con paseos diarios por el parque de Doña Casilda.',
                'hotel_owner': hotel_owner,
            },
            {
                'name': 'CostaCan Málaga',
                'address': 'Paseo Marítimo Pablo Ruiz Picasso 58',
                'city': 'Málaga',
                'description': 'Residencia con piscina para perros y acceso a playa canina, perfecta para vacaciones de tu mascota.',
                'hotel_owner': hotel_owner,
            }
        ]



        for hotel_data in hotels:
            hotel = Hotel.objects.create(**hotel_data)
            self.stdout.write(self.style.SUCCESS(f'Hotel {hotel.name} creado exitosamente'))

