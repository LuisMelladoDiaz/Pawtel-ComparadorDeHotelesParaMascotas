from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.serializers import HotelSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class HotelOwnerViewSet(viewsets.ModelViewSet):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerSerializer

    def list(self, request):
        hotel_owners = HotelOwner.objects.filter(is_active=True)
        serializer = HotelOwnerSerializer(hotel_owners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(request, pk)
        serializer = HotelOwnerSerializer(hotel_owner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        input_serializer = HotelOwnerService.serialize_input_hotel_owner_create(request)
        HotelOwnerService.validate_create_hotel_owner(input_serializer, request.user)
        hotel_owner_created = HotelOwnerService.create_hotel_owner(input_serializer)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner_created
        )
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        input_serializer = HotelOwnerService.serialize_input_hotel_owner_update(
            request, pk
        )
        HotelOwnerService.validate_semantically_update_hotel_owner(pk, input_serializer)
        hotel_owner_updated = HotelOwnerService.update_hotel_owner(pk, input_serializer)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner_updated
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        input_serializer = HotelOwnerService.serialize_input_hotel_owner_partial_update(
            request, pk
        )
        HotelOwnerService.validate_semantically_partial_update_hotel_owner(
            pk, input_serializer
        )
        hotel_owner_updated = HotelOwnerService.partial_update_hotel_owner(
            pk, input_serializer
        )
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner_updated
        )
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        HotelOwnerService.delete_hotel_owner(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="hotels/get",
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
