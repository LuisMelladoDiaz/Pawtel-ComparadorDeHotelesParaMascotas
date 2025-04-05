from inspect import currentframe

from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.serializers import HotelSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class HotelOwnerViewSet(viewsets.ModelViewSet):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerSerializer

    # Default CRUD -----------------------------------------------------------

    def list(self, request):
        action_name = currentframe().f_code.co_name
        role_user = HotelOwnerService.authorize_action_hotel_owner(request, action_name)
        is_admin = role_user.user.role == UserRole.ADMIN
        hotel_owners = HotelOwnerService.list_hotel_owners(allow_inactive=is_admin)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owners, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        role_user = HotelOwnerService.authorize_action_hotel_owner(request, action_name)
        is_admin = role_user.user.role == UserRole.ADMIN
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(
            pk, allow_inactive=is_admin
        )
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        # It will be managed through the views of AuthApp
        raise MethodNotAllowed("Esta operación no está permitida")

    def update(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        hotel_owner = HotelOwnerService.authorize_action_hotel_owner(
            request, action_name, pk, True
        )
        AppUserService.general_update_app_user(request, hotel_owner.user.id)
        hotel_owner_updated = HotelOwnerService.retrieve_hotel_owner(pk)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner_updated
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        role_user = HotelOwnerService.authorize_action_hotel_owner(
            request, action_name, pk, True
        )
        is_admin = role_user.user.role == UserRole.ADMIN
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(
            pk, allow_inactive=is_admin
        )
        delete = HotelOwnerService.validate_all_hotels_deletion(pk)
        if delete:
            AppUserService.general_delete_app_user(request, hotel_owner.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            AppUserService.general_deactivate_app_user(request, hotel_owner.user.id)
            return Response(
                {
                    "detail": "Dueño de hotel archivado en vez de eliminado por reservas pasadas."
                },
                status=status.HTTP_200_OK,
            )

    # Get all hotels of hotel owner ------------------------------------------

    @action(
        detail=True,
        methods=["get"],
        url_path="hotels",
        url_name="list_hotels_of_hotel_owner_explicit",
    )
    def list_hotels_of_hotel_owner_explicit(self, request, pk=None):
        # Explicitly recieving the PK in the route (for admin)
        action_name = currentframe().f_code.co_name
        HotelOwnerService.authorize_action_hotel_owner(request, action_name, pk, True)
        return HotelOwnerViewSet.__list_hotels_of_hotel_owner_base(pk, request)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-hotels",
        url_name="list_hotels_of_hotel_owner_implicit",
    )
    def list_hotels_of_hotel_owner_implicit(self, request):
        # Implicitly recieving the PK via the authorized user (prefered)
        action_name = currentframe().f_code.co_name
        hotel_owner = HotelOwnerService.authorize_action_hotel_owner(
            request, action_name
        )
        return HotelOwnerViewSet.__list_hotels_of_hotel_owner_base(
            hotel_owner.id, request
        )

    @staticmethod
    def __list_hotels_of_hotel_owner_base(pk, request):
        # Common logic between both implicit and explicit
        hotels = HotelOwnerService.list_hotels_of_hotel_owner(pk)
        serializer = HotelSerializer(hotels, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete all hotels of hotel owner ---------------------------------------

    @action(
        detail=True,
        methods=["delete"],
        url_path="hotels/delete",
        url_name="delete_all_hotels_of_hotel_owner_explicit",
    )
    # Explicitly recieving the PK in the route (not for admin, just in case)
    def delete_all_hotels_of_hotel_owner_explicit(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelOwnerService.authorize_action_hotel_owner(request, action_name, pk, True)
        return HotelOwnerViewSet.__delete_all_hotels_of_hotel_owner_base(pk)

    @action(
        detail=False,
        methods=["delete"],
        url_path="my-hotels/delete",  # must add final /
        url_name="delete_all_hotels_of_hotel_owner_implicit",
    )
    def delete_all_hotels_of_hotel_owner_implicit(self, request, pk=None):
        # Implicitly recieving the PK via the authorized user (prefered)
        action_name = currentframe().f_code.co_name
        hotel_owner = HotelOwnerService.authorize_action_hotel_owner(
            request, action_name
        )
        return HotelOwnerViewSet.__delete_all_hotels_of_hotel_owner_base(hotel_owner.id)

    @staticmethod
    def __delete_all_hotels_of_hotel_owner_base(pk=None):
        # Common logic between both implicit and explicit
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
        action_name = currentframe().f_code.co_name
        HotelOwnerService.authorize_action_hotel_owner(request, action_name)
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
        url_path="approve",
        url_name="approve_hotel_owner_patch",
    )
    def approve_hotel_owner_patch(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelOwnerService.authorize_action_hotel_owner(request, action_name, pk)

        hotel_owner = HotelOwnerService.approve_hotel_owner_patch(pk)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["delete"],
        url_path="delete-unapproved",
        url_name="delete_unapproved_hotel_owner",
    )
    def delete_unapproved_hotel_owner(self, request, pk=None):
        action_name = currentframe().f_code.co_name
        HotelOwnerService.authorize_action_hotel_owner(request, action_name, pk)

        HotelOwnerService.delete_unapproved_hotel_owner(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
