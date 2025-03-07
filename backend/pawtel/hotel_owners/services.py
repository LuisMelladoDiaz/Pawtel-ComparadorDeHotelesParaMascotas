from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import PermissionDenied


class HotelOwnerService:

    def check_if_active(hotel_owner_id):
        try:
            hotel_owner = HotelOwner.objects.get(id=hotel_owner_id)
            if not hotel_owner.is_active:
                raise PermissionDenied(
                    "El propietario del hotel está inactivo. No se puede realizar esta operación."
                )
        except HotelOwner.DoesNotExist:
            raise PermissionDenied("El propietario del hotel no existe.")

    def get_all_hotels_of_hotel_owner(hotel_owner_id):
        hotel_owner = HotelOwner.objects.get(id=hotel_owner_id)
        return Hotel.objects.filter(hotel_owner=hotel_owner)

    def delete_all_hotels_of_hotel_owner(hotel_owner_id):
        hotel_owner = HotelOwner.objects.get(id=hotel_owner_id)
        hotels_deleted, _ = Hotel.objects.filter(hotel_owner=hotel_owner).delete()
        return hotels_deleted
