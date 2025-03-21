from pawtel.app_users.services import AppUserService
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.customers.serializers import CustomerSerializer
from rest_framework.exceptions import NotFound, PermissionDenied


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
        logged_in_customer = CustomerService.get_current_customer(request)

        if pk:
            target_customer = CustomerService.retrieve_customer(pk)
            AppUserService.retrieve_app_user(target_customer.user_id)

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
            if allow_inactive:
                return Customer.objects.get(id=pk)
            else:
                return Customer.objects.get(id=pk, user__is_active=True)
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found.")

    @staticmethod
    def get_customer_by_user(app_user_id):
        try:
            return Customer.objects.get(user_id=app_user_id)
        except Customer.DoesNotExist:
            raise NotFound("Customer does not exist.")

    @staticmethod
    def get_current_customer(request):
        app_user = AppUserService.get_current_app_user(request)
        customer = CustomerService.get_customer_by_user(app_user)
        return customer

    @staticmethod
    def list_customers(allow_inactive=False):
        if allow_inactive:
            return Customer.objects.all()
        else:
            return Customer.objects.filter(user__is_active=True)

    @staticmethod
    def list_bookings_of_customer(customer_id):
        return Booking.objects.filter(customer_id=customer_id)

    # POST -------------------------------------------------------------------

    @staticmethod
    def __create_customer(app_user_id):
        return Customer.objects.create(user_id=app_user_id)
