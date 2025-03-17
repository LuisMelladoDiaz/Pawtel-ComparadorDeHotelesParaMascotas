from pawtel.app_users.services import AppUserService
from pawtel.customers.models import Customer
from pawtel.customers.serializers import CustomerSerializer
from rest_framework.exceptions import (AuthenticationFailed, NotFound,
                                       PermissionDenied)


class CustomerService:

    @staticmethod
    def check_permission(user, action):
        customer_permissions = {
            # list temporal
            "allowed_actions": [
                "list",
                "retrieve",
                "update",
                "partial_update",
                "destroy",
                "retrieve_current_customer",
            ],
            "denied_actions": ["create"],
        }

        hotel_owner_permissions = {
            "allowed_actions": [],
            "denied_actions": [
                "create",
                "update",
                "partial_update",
                "destroy",
                "retrieve_current_customer",
                "list",
                "retrieve",
            ],
        }

        """
        app_admin_permissions = {
            'allowed_actions': ['list', 'retrieve'],
            'denied_actions': ['create', 'update', 'partial_update', 'destroy', 'retrieve_current_customer']
        }
        """

        if hasattr(user, "customer"):
            permissions = customer_permissions
            user_type = "Customer"
        elif hasattr(user, "hotelowner"):
            permissions = hotel_owner_permissions
            user_type = "HotelOwner"
            """
        elif hasattr(user, "app_admin"):
            permissions = app_admin_permissions
            user_type = "AppAdmin"
        """
        else:
            raise PermissionDenied("Role not recognized.")

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
    def general_create_customer(request):
        """This will be called from the views of AuthApp."""
        app_user = AppUserService.general_create_app_user(request)
        customer_created = CustomerService.__create_customer(app_user.id)
        output_serializer_data = CustomerService.serialize_output_customer(
            customer_created
        )
        return output_serializer_data

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_customer(request, pk, permission_granted, user_type):
        if permission_granted:
            # if not user_type == "AppAdmin":
            target_customer = CustomerService.retrieve_customer(pk)
            if not target_customer:
                raise NotFound("Customer does not exist.")
            target_app_user = AppUserService.retrieve_app_user(target_customer.user_id)
            logged_in_customer = CustomerService.get_current_customer(
                request, permission_granted, user_type
            )

            if (not target_app_user) or (not target_app_user.is_active):
                raise NotFound("Customer does not exist.")

            if target_customer.id != logged_in_customer.id:
                raise PermissionDenied("Permission denied.")
            """   else:
                    target_customer = CustomerService.retrieve_customer(pk)
                    if not target_customer:
                        raise NotFound("Customer does not exist.")"""

    @staticmethod
    def serialize_output_customer(customer, many=False):
        return CustomerSerializer(customer, many=many).data

    @staticmethod
    def get_app_user_id_of_customer(customer_id):
        return CustomerService.retrieve_customer(customer_id).user.id

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_customer(pk):
        return Customer.objects.get(id=pk)

    @staticmethod
    def list_customers(permission_granted, user_type):
        if permission_granted:
            # if not user_type =="AppAdmin":
            return Customer.objects

    # POST -------------------------------------------------------------------

    @staticmethod
    def __create_customer(app_user_id):
        return Customer.objects.create(user_id=app_user_id)

    # Other -------------------------------------------------------------------

    @staticmethod
    def get_current_customer(request, permission_granted, user_type):
        if permission_granted and user_type == "Customer":
            if (not request.user) or (not request.user.is_authenticated):
                raise AuthenticationFailed("User is not authenticated.")
            customer = Customer.objects.get(user_id=request.user.id)
            return customer
