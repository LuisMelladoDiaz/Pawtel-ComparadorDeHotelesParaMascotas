from datetime import date, timedelta

from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer
from pawtel.customers.serializers import CustomerSerializer
from pawtel.permission_services import PermissionService
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class CustomerService:

    THREE_YEARS = timedelta(days=3 * 365)

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

    # Authorization ----------------------------------------------------------

    def authorize_action_customer(
        request, action_name, target_customer_id=None, check_ownership=False
    ):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_customer_service(role_user, action_name)

        if target_customer_id:
            target_customer = CustomerService.__perform_retrieve_customer(
                role_user, target_customer_id
            )
            if check_ownership:
                CustomerService.__check_ownership_customer(role_user, target_customer)

        return role_user

    def __perform_retrieve_customer(role_user, target_customer_id):
        if role_user.user.role == UserRole.ADMIN:
            return CustomerService.retrieve_customer(
                target_customer_id, allow_inactive=True
            )
        else:
            return CustomerService.retrieve_customer(target_customer_id)

    def __check_ownership_customer(role_user, target_customer):
        if role_user.user.role == UserRole.ADMIN:
            return
        elif role_user.user.role == UserRole.CUSTOMER:
            if target_customer.id != role_user.id:
                raise PermissionDenied("Permiso denegado.")
        else:
            raise PermissionDenied("Permiso denegado.")

    # Serialization -----------------------------------------------------------------

    @staticmethod
    def serialize_output_customer(customer, many=False):
        return CustomerSerializer(customer, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_customer(pk, allow_inactive=False):
        try:
            if allow_inactive:
                return Customer.objects.get(id=pk)
            else:
                return Customer.objects.get(id=pk, user__is_active=True)
        except Customer.DoesNotExist:
            raise NotFound(detail="Cliente no encontrado.")

    @staticmethod
    def get_customer_by_user(app_user_id):
        try:
            return Customer.objects.get(user_id=app_user_id)
        except Customer.DoesNotExist:
            raise NotFound("El cliente no existe.")

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

    # DELETE -----------------------------------------------------------------

    def validate_customer_deletion(pk):
        today = date.today()
        past_limit = today - CustomerService.THREE_YEARS
        delete = True

        recent_bookings = Booking.objects.filter(
            customer_id=pk, start_date__range=(past_limit, today)
        )
        future_bookings = Booking.objects.filter(customer_id=pk, start_date__gte=today)

        if future_bookings.exists():
            raise ValidationError(
                {
                    "detail": "No se puede eliminar el objeto porque tiene una reserva asociada próximamente."
                }
            )

        if recent_bookings.exists():
            delete = False

        return delete
