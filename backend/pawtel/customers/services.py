from pawtel.app_users.services import AppUserService
from pawtel.customers.models import Customer
from pawtel.customers.serializers import CustomerSerializer
from rest_framework.exceptions import (AuthenticationFailed, NotFound,
                                       PermissionDenied)


class CustomerService:

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
    def authorize_action_customer(request, pk):
        target_customer = CustomerService.retrieve_customer(pk)
        if not target_customer:
            raise NotFound("Customer does not exist.")
        target_app_user = AppUserService.retrieve_app_user(target_customer.user_id)
        logged_in_customer = CustomerService.get_current_customer(request)

        if (not target_app_user) or (not target_app_user.is_active):
            raise NotFound("Customer does not exist.")

        if target_customer.id != logged_in_customer.id:
            raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_output_customer(customer, many=False):
        return CustomerSerializer(customer, many=many).data

    @staticmethod
    def get_app_user_id_of_customer(customer_id):
        return CustomerService.retrieve_customer(customer_id).user.id

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_customer(pk, allow_inactive=False):
        try:
            return Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found.")

    @staticmethod
    def list_customers():
        return Customer.objects

    # POST -------------------------------------------------------------------

    @staticmethod
    def __create_customer(app_user_id):
        return Customer.objects.create(user_id=app_user_id)

    # Other -------------------------------------------------------------------

    @staticmethod
    def get_current_customer(request):
        if (not request.user) or (not request.user.is_authenticated):
            raise AuthenticationFailed("User is not authenticated.")
        
        customer = Customer.objects.get(user_id=request.user.id)
        if (not customer) or (not customer.user.is_active):
            raise NotFound("Customer does not exist.")
        
        return customer
