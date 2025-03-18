from pawtel.app_users.services import AppUserService
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.models import Customer
from pawtel.customers.serializers import CustomerSerializer
from pawtel.customers.services import CustomerService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        customers = CustomerService.list_customers()
        output_serializer_data = CustomerService.serialize_output_customer(
            customers, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        CustomerService.authorize_action_customer(request, pk)
        customer = CustomerService.retrieve_customer(pk)
        output_serializer_data = CustomerService.serialize_output_customer(customer)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        # It will be managed through the views of AuthApp
        raise PermissionDenied("This operation is forbidden.")

    def update(self, request, pk=None):
        CustomerService.authorize_action_customer(request, pk)
        app_user_id = CustomerService.get_app_user_id_of_customer(pk)
        AppUserService.general_update_app_user(request, app_user_id)
        customer_updated = CustomerService.retrieve_customer(pk)
        output_serializer_data = CustomerService.serialize_output_customer(
            customer_updated
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        CustomerService.authorize_action_customer(request, pk)
        app_user_id = CustomerService.get_app_user_id_of_customer(pk)
        AppUserService.general_delete_app_user(request, app_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="retrieve_current_customer",
    )
    def retrieve_current_customer(self, request):
        hotel_owner = CustomerService.get_current_hotel_owner(request)
        output_serializer_data = CustomerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="bookings",
        url_name="get_all_bookings_by_customer_explicit",
    )
    def get_all_bookings_by_customer_explicit(self, request, pk=None):
        CustomerService.authorize_action_customer(request, pk)
        bookings = CustomerService.get_all_bookings_by_customer(pk, request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-bookings",
        url_name="get_all_bookings_by_customer_implicit",
    )
    def get_all_bookings_by_customer_implicit(self, request):
        customer = CustomerService.get_current_customer(request)
        bookings = CustomerService.get_all_bookings_by_customer(
            customer.id, request.user
        )
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
