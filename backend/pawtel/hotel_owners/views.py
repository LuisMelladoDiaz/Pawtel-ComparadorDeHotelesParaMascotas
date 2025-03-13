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

    def list(self, request):
        hotel_owners = HotelOwnerService.list_hotel_owners()
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owners, many=True
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        # It will be managed through the views of AuthApp
        raise PermissionDenied("This operation is forbidden.")

    def update(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
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
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        app_user_id = HotelOwnerService.get_app_user_id_of_hotel_owner(pk)
        AppUserService.general_delete_app_user(request, app_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotels",
        url_name="get_all_hotels_of_hotel_owner",
    )
    def get_all_hotels_of_hotel_owner(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(pk)
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["delete"],
        url_path="hotels/delete",
        url_name="delete_all_hotels_of_hotel_owner",
    )
    def delete_all_hotels_of_hotel_owner(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        HotelOwnerService.delete_all_hotels_of_hotel_owner(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        url_path="hotel-owners-me",
        url_name="retrieve_current_hotel_owner",
    )
    def retrieve_current_hotel_owner(self, request):
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)
