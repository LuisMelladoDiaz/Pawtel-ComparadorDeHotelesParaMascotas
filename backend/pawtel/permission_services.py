from pawtel.app_users.models import UserRole
from rest_framework.exceptions import PermissionDenied


class PermissionService:

    ADMIN_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {},
        UserRole.HOTEL_OWNER.value: {},
        UserRole.ADMIN.value: {
            "list",
            "retrieve",
            "destroy",
            "update",
            "partial_update",
        },
    }

    BOOKING_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {
            "retrieve",
        },
        UserRole.HOTEL_OWNER.value: {
            "retrieve",
        },
        UserRole.ADMIN.value: {"list", "retrieve"},
    }

    BOOKING_HOLD_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {
            "retrieve",
            "create",
            "destroy",
        },
        UserRole.HOTEL_OWNER.value: {},
        UserRole.ADMIN.value: {"list", "retrieve", "destroy"},
    }

    CUSTOMER_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "retrieve_current_customer",
            "list_bookings_of_customer_explicit",
            "list_bookings_of_customer_implicit",
        },
        UserRole.HOTEL_OWNER.value: {},
        UserRole.ADMIN.value: {
            "list",
            "retrieve",
            "list_bookings_of_customer_explicit",
            "destroy",
        },
    }

    HOTEL_OWNER_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {},
        UserRole.HOTEL_OWNER.value: {
            "retrieve",
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
            "approve_hotel_owner_patch",
            "destroy",
            "delete_unapproved_hotel_owner",
            "list_unapproved_hotel_owners",
        },
    }

    HOTEL_SERVICE_PERMISSIONS = {
        UserRole.CUSTOMER.value: {
            "list",
            "retrieve",
            "list_room_types_of_hotel",
            "get_cover_image",
            "get_non_cover_images",
        },
        UserRole.HOTEL_OWNER.value: {
            "list",
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
            "list_room_types_of_hotel",
            "list_bookings_of_hotel",
            "list_images_of_hotel",
            "retrieve_image",
            "update_image",
            "upload_image",
            "partial_update_image",
            "destroy_image",
            "get_cover_image",
            "get_non_cover_images",
            "set_image_is_cover",
        },
        UserRole.ADMIN.value: {
            "list",
            "retrieve",
            "list_room_types_of_hotel",
            "list_bookings_of_hotel",
            "list_images_of_hotel",
            "retrieve_image",
            "get_cover_image",
            "get_non_cover_images",
            "destroy",
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
            "destroy",
        },
    }

    @staticmethod
    def __base_check_role_permission(role_user, action, permissions_dict):
        role = role_user.user.role
        if action not in permissions_dict.get(role, {}):
            raise PermissionDenied(f"Permission denied for action: {action}.")

    @staticmethod
    def check_permission_admin_service(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.ADMIN_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_permission_booking_service(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.BOOKING_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_permission_booking_hold_service(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.BOOKING_HOLD_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_permission_customer_service(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.CUSTOMER_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_permission_hotel_owner_service(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.HOTEL_OWNER_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_permission_hotel_service(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.HOTEL_SERVICE_PERMISSIONS
        )

    @staticmethod
    def check_permission_room_type_service(role_user, action):
        PermissionService.__base_check_role_permission(
            role_user, action, PermissionService.ROOM_TYPE_SERVICE_PERMISSIONS
        )
