from pawtel.app_users.models import UserRole
from rest_framework.exceptions import PermissionDenied


class PermissionService:

    BOOKING_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {
            "list",  ##! TODO: remove when Admin added; kept for test
            "retrieve",
        },
        UserRole.HOTEL_OWNER.value: {
            "retrieve",
        },
        UserRole.ADMIN.value: {
            "list",
            "retrieve",
        },
    }

    HOTEL_OWNER_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {},
        UserRole.HOTEL_OWNER.value: {
            "list",  ##! TODO: remove when Admin added; kept for test
            "retrieve",
            "create",  ##! TODO: remove when Admin added; kept for test
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

    ROOM_TYPE_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {
            "retrieve",
            "is_room_type_available",
            "get_hotel_of_room_type",
        },
        UserRole.HOTEL_OWNER.value: {
            "list",
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
            "is_room_type_available",
            "get_hotel_of_room_type",
        },
        UserRole.ADMIN.value: {
            "list",
            "retrieve",
            "is_room_type_available",
            "get_hotel_of_room_type",
        },
    }

    @staticmethod
    def __base_check_role_permission(role_user, action, permissions_dict):
        role = role_user.user.role
        if action not in permissions_dict.get(role, {}):
            raise PermissionDenied(f"Permission denied for action: {action}.")

    @staticmethod
    def check_booking_role_permission(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.BOOKING_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_hotel_owner_role_permission(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.HOTEL_OWNER_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_room_type_role_permission(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.ROOM_TYPE_SERVICE_PERMISSIONS
        )
