from pawtel.app_users.models import UserRole
from rest_framework.exceptions import PermissionDenied


class PermissionService:

    HOTEL_OWNER_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {},
        UserRole.HOTEL_OWNER.value: {
            "list",
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
            "list_hotels_of_hotel_owner_explicit",
            "list_hotels_of_hotel_owner_implicit",
            "delete_all_hotels_of_hotel_owner_explicit",
            "delete_all_hotels_of_hotel_owner_implicit",
            "retrieve_current_hotel_owner",
        },
        UserRole.ADMIN.value: {
            "list",
            "retrieve",
            "list_hotels_of_hotel_owner_explicit",
        },
    }

    @staticmethod
    def __base_check_role_permission(role_user, action, permissions_dict):
        role = role_user.user.role
        if action not in permissions_dict.get(role, {}):
            raise PermissionDenied(f"Permission denied for action: {action}.")

    @staticmethod
    def check_hotel_owner_role_permission(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.HOTEL_OWNER_SERVICE_PERMISSIONS
        )
