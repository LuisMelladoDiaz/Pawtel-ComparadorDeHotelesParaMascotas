from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from pawtel.customers.services import CustomerService
from rest_framework.exceptions import NotFound, PermissionDenied


class BookingService:

    def check_permission(user, action):
        customer_permissions = {
            # List temporal
            "allowed_actions": ["list", "retrieve"],
            "denied_actions": [
                "create",
                "update",
                "partial_update",
                "destroy",
            ],
        }

        hotel_owner_permissions = {
            "allowed_actions": ["retrieve"],
            "denied_actions": ["list", "create", "update", "partial_update", "destroy"],
        }

        """
        app_admin_permissions = {
            'allowed_actions': ['list', 'retrieve'],
            'denied_actions': ['create', 'update', 'partial_update', 'destroy']
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

    # Common ------------------------------------------------------------

    @staticmethod
    def serialize_output_booking(booking, many=False):
        return BookingSerializer(booking, many=many).data

    # Authorization -----------------------------------------------------

    @staticmethod
    def authorize_action_booking(request, pk, permission_granted, user_type):
        if permission_granted:
            if not user_type == "AppAdmin":
                booking = BookingService.retrieve_booking(pk)
                customer = CustomerService.get_current_customer(
                    request, permission_granted, user_type
                )
                if not booking:
                    raise NotFound("Booking does not exist.")

                if booking.customer.id != customer.id:
                    raise PermissionDenied("Permission denied.")
            else:
                booking = BookingService.retrieve_booking(pk)
                if not booking:
                    raise NotFound("Booking does not exist.")

    #  GET Methods --------------------------------------------------------

    @staticmethod
    def list_bookings(permission_granted, user_type):
        if permission_granted:
            # if user_type == "AppAdmin":
            bookings = Booking.objects.all()
            return bookings

    @staticmethod
    def retrieve_booking(pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound(detail=f"Booking with id {pk} not found")
