import inspect

from pawtel.app_users.services import AppUserService
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.serializers import HotelSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class HotelOwnerViewSet(viewsets.ModelViewSet):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerSerializer

    # Default CRUD -----------------------------------------------------------

    def list(self, request):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        hotel_owners = HotelOwnerService.list_hotel_owners(
            permission_granted, user_type
        )
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owners, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        HotelOwnerService.authorize_action_hotel_owner(
            request, pk, permission_granted, user_type
        )
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        # It will be managed through the views of AuthApp
        raise PermissionDenied("This operation is forbidden.")

    def update(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        HotelOwnerService.authorize_action_hotel_owner(
            request, pk, permission_granted, user_type
        )
        app_user_id = HotelOwnerService.get_app_user_id_of_hotel_owner(pk)
        AppUserService.general_update_app_user(request, app_user_id)
        hotel_owner_updated = HotelOwnerService.retrieve_hotel_owner(pk)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner_updated
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        HotelOwnerService.authorize_action_hotel_owner(
            request, pk, permission_granted, user_type
        )
        app_user_id = HotelOwnerService.get_app_user_id_of_hotel_owner(pk)
        AppUserService.general_delete_app_user(request, app_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Get all hotels of hotel owner ------------------------------------------

    @action(
        detail=True,
        methods=["get"],
        url_path="hotels",
        url_name="get_all_hotels_of_hotel_owner_explicit",
    )
    def get_all_hotels_of_hotel_owner_explicit(self, request, pk=None):
        # Same as get_all_hotels_of_hotel_owner_implicit, but explicitly recieving the PK in the route (kept for admin)
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        HotelOwnerService.authorize_action_hotel_owner(
            request, pk, permission_granted, user_type
        )
        return HotelOwnerViewSet.__get_all_hotels_of_hotel_owner_base(pk)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-hotels",
        url_name="get_all_hotels_of_hotel_owner_implicit",
    )
    def get_all_hotels_of_hotel_owner_implicit(self, request):
        # Same as get_all_hotels_of_hotel_owner_explicit, but implicitly recieving the PK via the authorized user (prefered)
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        HotelOwnerService.authorize_action_hotel_owner(
            request, pk=None, permission_granted=permission_granted, user_type=user_type
        )
        hotel_owner_id = HotelOwnerService.get_current_hotel_owner(
            request, permission_granted
        ).id
        return HotelOwnerViewSet.__get_all_hotels_of_hotel_owner_base(hotel_owner_id)

    @staticmethod
    def __get_all_hotels_of_hotel_owner_base(pk):
        # Common logic between both methods
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(pk)
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete all hotels of hotel owner ---------------------------------------

    @action(
        detail=True,
        methods=["delete"],
        url_path="hotels/delete",
        url_name="delete_all_hotels_of_hotel_owner_explicit",
    )
    # Same as get_all_hotels_of_hotel_owner_implicit, but explicitly recieving the PK in the route (kept for admin)
    def delete_all_hotels_of_hotel_owner_explicit(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        HotelOwnerService.authorize_action_hotel_owner(
            request, pk, permission_granted, user_type
        )
        return HotelOwnerViewSet.__delete_all_hotels_of_hotel_owner_base(pk)

    @action(
        detail=False,
        methods=["delete"],
        url_path="my-hotels/delete",  # must add final /
        url_name="delete_all_hotels_of_hotel_owner_implicit",
    )
    def delete_all_hotels_of_hotel_owner_implicit(self, request, pk=None):
        # Same as delete_all_hotels_of_hotel_owner_explicit, but implicitly recieving the PK via the authorized user (prefered)
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        HotelOwnerService.authorize_action_hotel_owner(
            request, pk, permission_granted, user_type
        )
        hotel_owner_id = HotelOwnerService.get_current_hotel_owner(
            request, permission_granted
        ).id
        return HotelOwnerViewSet.__delete_all_hotels_of_hotel_owner_base(hotel_owner_id)

    @staticmethod
    def __delete_all_hotels_of_hotel_owner_base(pk=None):
        # Common logic between both methods
        HotelOwnerService.delete_all_hotels_of_hotel_owner(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Others -----------------------------------------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="retrieve_current_hotel_owner",
    )
    def retrieve_current_hotel_owner(self, request):
        action_name = inspect.currentframe().f_code.co_name
        permission_granted, user_type = HotelOwnerService.check_permission(
            request.user, action_name
        )
        hotel_owner = HotelOwnerService.get_current_hotel_owner(
            request, permission_granted
        )
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)
