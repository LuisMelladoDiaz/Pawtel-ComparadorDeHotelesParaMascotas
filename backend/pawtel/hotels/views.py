from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer
from pawtel.hotels.services import HotelService
from pawtel.room_types.serializers import RoomTypeSerializer
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.bookings.models import Booking
from pawtel.bookings.serializers import BookingSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def list(self, request):
        filters = request.query_params.dict()  # URL filters checked
        hotels = HotelService.list_hotels(filters)
        output_serializer_data = HotelService.serialize_output_hotel(hotels, many=True)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        hotel = HotelService.retrieve_hotel(pk)
        output_serializer_data = HotelService.serialize_output_hotel(hotel)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        input_serializer = HotelService.serialize_input_hotel_create(request)
        HotelService.validate_create_hotel(input_serializer)
        hotel_created = HotelService.create_hotel(input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(hotel_created)
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        input_serializer = HotelService.serialize_input_hotel_update(request, pk)
        HotelService.validate_update_hotel(pk, input_serializer)
        hotel_updated = HotelService.update_hotel(pk, input_serializer)
        output_serializer_data = HotelService.serialize_output_hotel(hotel_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # The context of the request specifies that it is PATCH
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        HotelService.delete_hotel(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_path="room-types",
        url_name="get_all_room_types_of_hotel",
    )
    def get_all_room_types_of_hotel(self, request, pk=None):
        HotelService.authorize_action_hotel(request, pk)
        room_types = HotelService.get_all_room_types_of_hotel(pk)
        serializer = RoomTypeSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=["get"],
        url_path="bookings",
        url_name="get_all_bookings_by_hotel_explicit",
    )
    def get_all_bookings_by_hotel_explicit(self, request, pk=None):
        HotelOwnerService.authorize_action_hotel_owner(request, pk)
        return HotelViewSet.__get_all_bookings_by_hotel_base(pk)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-bookings",
        url_name="get_all_bookings_by_hotel_implicit",
    )
    def get_all_bookings_by_hotel_implicit(self, request):
        HotelOwnerService.authorize_action_hotel_owner(request)
        hotel_owner_id = HotelOwnerService.get_current_hotel_owner(request).id
        hotels = HotelOwnerService.get_all_hotels_of_hotel_owner(hotel_owner_id)
        
        bookings = []
        for hotel in hotels:
            bookings.extend(HotelService.get_all_bookings_by_hotel(hotel.id))

        return HotelViewSet.__serialize_bookings(bookings)

    @staticmethod
    def __get_all_bookings_by_hotel_base(hotel_id):
        bookings = HotelService.get_all_bookings_by_hotel(hotel_id)
        return HotelViewSet.__serialize_bookings(bookings)

    @staticmethod
    def __serialize_bookings(bookings):
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
