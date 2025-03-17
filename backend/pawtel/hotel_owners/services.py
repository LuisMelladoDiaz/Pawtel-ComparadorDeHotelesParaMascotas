from pawtel.app_users.services import AppUserService
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import (AuthenticationFailed, NotFound,
                                       PermissionDenied)

# to get the current hotel owner


class HotelOwnerService:

    def check_permission(user, action):
        """Checks if the user has permission to perform an action based on their type."""

        customer_permissions = {
            "allowed_actions": [],
            "denied_actions": [
                "list",
                "retrieve",
                "create",
                "update",
                "destroy",
                "get_all_hotels_of_hotel_owner_explicit",
                "get_all_hotels_of_hotel_owner_implicit",
                "delete_all_hotels_of_hotel_owner_explicit",
                "delete_all_hotels_of_hotel_owner_implicit",
                "retrieve_current_hotel_owner",
            ],
        }

        hotel_owner_permissions = {
            "allowed_actions": [
                "retrieve",
                "update",
                "destroy",
                "get_all_hotels_of_hotel_owner_implicit",
                "delete_all_hotels_of_hotel_owner_implicit",
                "retrieve_current_hotel_owner",
                "list",
                "create",
                "get_all_hotels_of_hotel_owner_implicit",
                "delete_all_hotels_of_hotel_owner_explicit",
                "get_all_hotels_of_hotel_owner_explicit",
            ],
            "denied_actions": [],
        }

        # Temporal hasta que esté admin
        """
        app_admin_permissions = {
            'allowed_actions': [
                'list', 'retrieve', 'create', 'update', 'destroy',
                'get_all_hotels_of_hotel_owner_explicit', 'get_all_hotels_of_hotel_owner_implicit',
                'delete_all_hotels_of_hotel_owner_explicit','delete_all_hotels_of_hotel_owner_implicit', 'retrieve_current_hotel_owner'
            ],
            'denied_actions': []
        }
        """

        if hasattr(user, "customer"):
            permissions = customer_permissions
            user_type = "Customer"
        elif hasattr(user, "hotelowner"):
            permissions = hotel_owner_permissions
            user_type = "HotelOwner"

            """ elif hasattr(user, "app_admin"):
            permissions = app_admin_permissions
            user_type = "AppAdmin" """

        else:
            raise PermissionDenied("Role not recognized.")

        # Verificar si la acción está permitida
        if action in permissions["allowed_actions"]:
            return True, user_type
        elif action in permissions["denied_actions"]:
            raise PermissionDenied(
                f"You don't have permission to perform the action: {action}"
            )
        else:
            raise PermissionDenied(f"Action {action} is not recognized for your role.")

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
    def authorize_action_hotel_owner(
        request, pk=None, permission_granted=None, user_type=None
    ):
        if permission_granted:
            # if not user_type == "AppAdmin":
            logged_in_hotel_owner = HotelOwnerService.get_current_hotel_owner(request)
            if pk:
                target_hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
                if not target_hotel_owner:
                    raise NotFound("Hotel owner does not exist.")
                target_app_user = AppUserService.retrieve_app_user(
                    target_hotel_owner.user_id
                )

                if (not target_app_user) or (not target_app_user.is_active):
                    raise NotFound("Hotel owner does not exist.")

                if target_hotel_owner.id != logged_in_hotel_owner.id:
                    raise PermissionDenied("Permission denied.")
            # else :
            """
                if pk:
                    target_hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
                    if not target_hotel_owner:
                        raise NotFound("Hotel owner does not exist.")"""

    @staticmethod
    def serialize_output_hotel_owner(hotel_owner, many=False):
        return HotelOwnerSerializer(hotel_owner, many=many).data

    @staticmethod
    def get_app_user_id_of_hotel_owner(hotel_owner_id):
        return HotelOwnerService.retrieve_hotel_owner(hotel_owner_id).user.id

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel_owner(pk):
        return HotelOwner.objects.get(id=pk)

    @staticmethod
    def list_hotel_owners(permission_granted, user_type):
        if not permission_granted:
            raise PermissionDenied(f"You don't have permission to perform the action")
        return HotelOwner.objects

    # POST -------------------------------------------------------------------

    @staticmethod
    def __create_hotel_owner(app_user_id):
        return HotelOwner.objects.create(user_id=app_user_id)

    # OTHERS -----------------------------------------------------------------

    @staticmethod
    def get_all_hotels_of_hotel_owner(hotel_owner_id):
        return Hotel.objects.filter(hotel_owner_id=hotel_owner_id, is_archived=False)

    @staticmethod
    def delete_all_hotels_of_hotel_owner(hotel_owner_id):
        hotels_to_delete = Hotel.objects.filter(
            hotel_owner_id=hotel_owner_id, is_archived=False
        )
        if not hotels_to_delete.exists():
            raise PermissionDenied("No hotels to delete.")

        hotels_to_delete.delete()

    @staticmethod
    def get_current_hotel_owner(request):
        if (not request.user) or (not request.user.is_authenticated):
            raise AuthenticationFailed("User is not authenticated.")
        hotel_owner = HotelOwner.objects.get(user_id=request.user.id)
        return hotel_owner
