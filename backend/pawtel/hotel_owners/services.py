from pawtel.app_users.services import AppUserService
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import NotFound, PermissionDenied


class HotelOwnerService:

    # General processes ------------------------------------------------------

    @staticmethod
    def general_create_hotel_owner(request):
        """This will be called from the views of AuthApp."""
        app_user = AppUserService.general_create_app_user(request)
        hotel_owner_created = HotelOwnerService.__create_hotel_owner(app_user.id)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner_created
        )
        return output_serializer_data

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_hotel_owner(request, pk=None):
        logged_in_hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        if pk:
            target_hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
            AppUserService.retrieve_app_user(target_hotel_owner.user_id)

            if target_hotel_owner.id != logged_in_hotel_owner.id:
                raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_output_hotel_owner(hotel_owner, many=False):
        return HotelOwnerSerializer(hotel_owner, many=many).data

    @staticmethod
    def get_app_user_id_of_hotel_owner(hotel_owner_id):
        return HotelOwnerService.retrieve_hotel_owner(hotel_owner_id).user.id

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel_owner(pk, allow_inactive=False):
        try:
            if allow_inactive:
                return HotelOwner.objects.get(id=pk)
            else:
                return HotelOwner.objects.get(id=pk, user__is_active=True)
        except HotelOwner.DoesNotExist:
            raise NotFound(detail="Hotel owner not found.")

    @staticmethod
    def get_hotel_owner_by_user(app_user_id):
        try:
            return HotelOwner.objects.get(user_id=app_user_id)
        except HotelOwner.DoesNotExist:
            raise NotFound("Hotel owner does not exist.")

    @staticmethod
    def get_current_hotel_owner(request):
        app_user = AppUserService.get_current_app_user(request)
        hotel_owner = HotelOwnerService.get_hotel_owner_by_user(app_user)
        return hotel_owner

    @staticmethod
    def list_hotel_owners(allow_inactive=False):
        if allow_inactive:
            return HotelOwner.objects.all()
        else:
            return HotelOwner.objects.filter(user__is_active=True)

    # POST -------------------------------------------------------------------

    @staticmethod
    def __create_hotel_owner(app_user_id):
        return HotelOwner.objects.create(user_id=app_user_id)

    # OTHERS -----------------------------------------------------------------

    @staticmethod
    def list_hotels_of_hotel_owner(hotel_owner_id):
        return Hotel.objects.filter(hotel_owner_id=hotel_owner_id, is_archived=False)

    @staticmethod
    def delete_all_hotels_of_hotel_owner(hotel_owner_id):
        hotels_to_delete = Hotel.objects.filter(
            hotel_owner_id=hotel_owner_id, is_archived=False
        )
        if not hotels_to_delete.exists():
            raise PermissionDenied("No hotels to delete.")

        hotels_to_delete.delete()
