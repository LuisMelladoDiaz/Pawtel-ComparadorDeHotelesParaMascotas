import inspect

from pawtel.app_users.services import AppUserService
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.models import Customer
from pawtel.customers.serializers import CustomerSerializer
from pawtel.customers.services import CustomerService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        action_name = inspect.currentframe().f_code.co_name
        CustomerService.authorize_action_customer_level_1(request, action_name)
        customers = CustomerService.list_customers()
        output_serializer_data = CustomerService.serialize_output_customer(
            customers, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        CustomerService.authorize_action_customer_level_3(request, pk, action_name)
        customer = CustomerService.retrieve_customer(pk)
        output_serializer_data = CustomerService.serialize_output_customer(customer)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        # It will be managed through the views of AuthApp
        raise MethodNotAllowed("This operation is forbidden.")

    def update(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        customer = CustomerService.authorize_action_customer_level_3(
            request, pk, action_name
        )
        AppUserService.general_update_app_user(request, customer.user.id)
        customer_updated = CustomerService.retrieve_customer(pk)
        output_serializer_data = CustomerService.serialize_output_customer(
            customer_updated
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        customer = CustomerService.authorize_action_customer_level_3(
            request, pk, action_name
        )
        if CustomerService.validate_customer_deletion(pk):
            AppUserService.general_delete_app_user(request, customer.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "message": "Customer archived instead of deleted due to past bookings."
                },
                status=status.HTTP_200_OK,
            )

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="retrieve_current_customer",
    )
    def retrieve_current_customer(self, request):
        customer = CustomerService.get_current_customer(request)
        output_serializer_data = CustomerService.serialize_output_customer(customer)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    # List bookings of customer ----------------------------------------------

    @action(
        detail=True,
        methods=["get"],
        url_path="bookings",
        url_name="list_bookings_of_customer_explicit",
    )
    def list_bookings_of_customer_explicit(self, request, pk=None):
        # Explicitly recieving the PK in the route (for admin)
        action_name = inspect.currentframe().f_code.co_name
        CustomerService.authorize_action_customer_level_3(request, pk, action_name)
        return CustomerViewSet.__list_bookings_of_customer_base(pk)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-bookings",
        url_name="list_bookings_of_customer_implicit",
    )
    def list_bookings_of_customer_implicit(self, request):
        # Implicitly recieving the PK via the authorized user (prefered)
        action_name = inspect.currentframe().f_code.co_name
        customer = CustomerService.authorize_action_customer_level_1(
            request, action_name
        )
        return CustomerViewSet.__list_bookings_of_customer_base(customer.id)

    @staticmethod
    def __list_bookings_of_customer_base(pk):
        # Common logic between both methods
        bookings = CustomerService.list_bookings_of_customer(pk)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Others -----------------------------------------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="retrieve_current_customer",
    )
    def retrieve_current_customer(self, request):
        action_name = inspect.currentframe().f_code.co_name
        CustomerService.authorize_action_customer_level_1(request, action_name)
        hotel_owner = CustomerService.get_current_customer(request)
        output_serializer_data = CustomerService.serialize_output_customer(hotel_owner)
        return Response(output_serializer_data, status=status.HTTP_200_OK)
