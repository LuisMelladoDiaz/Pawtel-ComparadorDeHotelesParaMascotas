from django.forms import ValidationError
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer
from pawtel.room_types.models import RoomType
from pawtel.rooms.models import Room
from rest_framework.exceptions import NotFound


class HotelService:

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_hotel(request, pk):
        hotel = HotelService.retrieve_hotel(pk)

        if (not hotel) or (hotel.is_archived):
            raise NotFound("Hotel does not exist.")

    @staticmethod
    def serialize_output_hotel(hotel, many=False):
        return HotelSerializer(hotel, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel(pk):
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise NotFound(detail=f"Hotel with id {pk} not found")

    # POST -------------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_create(request):
        context = {"request": request}
        current_owner_id = HotelOwnerService.get_current_hotel_owner(request).id
        data = request.data.copy()
        data["hotel_owner"] = current_owner_id
        serializer = HotelSerializer(data=data, context=context)
        return serializer

    @staticmethod
    def validate_create_hotel(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")
        hotel_owner_id = input_serializer.validated_data.get("hotel_owner").id

        if not HotelOwnerService.retrieve_hotel_owner(hotel_owner_id).user.is_active:
            raise ValidationError({"hotel_owner": "Invalid hotel owner."})

        if name and Hotel.objects.filter(name=name).exists():
            raise ValidationError({"name": "Name in use."})

    @staticmethod
    def create_hotel(input_serializer):
        hotel_created = input_serializer.save()
        return hotel_created

    # PUT/PATCH --------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_update(request, pk):
        hotel = HotelService.retrieve_hotel(pk)
        context = {"request": request}
        serializer = HotelSerializer(instance=hotel, data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_update_hotel(pk, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")

        if name and Hotel.objects.filter(name=name).exclude(id=pk).exists():
            raise ValidationError({"name": "Name in use."})

    @staticmethod
    def update_hotel(pk, input_serializer):
        hotel = HotelService.retrieve_hotel(pk)
        return input_serializer.update(hotel, input_serializer.validated_data)

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_hotel(pk):
        hotel = HotelService.retrieve_hotel(pk)
        hotel.delete()

    # Filter -----------------------------------------------------------------

    @staticmethod
    def list_hotels(filters=None):
        hotels = Hotel.objects.filter(is_archived=False)

        valid_filters = [
            "city",
            "name",
            "hotel_owner",
            "room_type",
            "max_price_per_night",
            "min_price_per_night",
            "sort_by",
            "limit",
        ]

        assert filters is None or all(f in valid_filters for f in filters), filters

        if filters:
            if "city" in filters:
                assert isinstance(filters["city"], str)
                hotels = hotels.filter(city__icontains=filters["city"])

            if "name" in filters:
                assert isinstance(filters["name"], str)
                hotels = hotels.filter(name__icontains=filters["name"])

            if "hotel_owner" in filters:
                hotels = hotels.filter(hotel_owner__id=filters["hotel_owner"])

            if "room_type" in filters:
                assert isinstance(filters["room_type"], str)
                hotels = hotels.filter(
                    roomtype__name__icontains=filters["room_type"]
                ).distinct()

            if "max_price_per_night" in filters:
                fl = float(filters["max_price_per_night"])
                assert isinstance(fl, float)
                try:
                    max_price = float(filters["max_price_per_night"])
                    hotels = hotels.filter(
                        roomtype__price_per_night__lte=max_price
                    ).distinct()
                except ValueError:
                    pass

            if "min_price_per_night" in filters:
                fl = float(filters["min_price_per_night"])
                assert isinstance(fl, float)
                try:
                    min_price = float(filters["min_price_per_night"])
                    hotels = hotels.filter(
                        roomtype__price_per_night__lte=min_price
                    ).distinct()
                except ValueError:
                    pass

            if "sort_by" in filters:
                assert isinstance(filters["sort_by"], str)
                # assert valid
                valid = ["price_per_night", "city", "name"]
                assert filters["sort_by"] in valid
                sort_field = filters["sort_by"]
                if sort_field.startswith("-"):  # Permitir orden descendente
                    hotels = hotels.order_by(sort_field)
                else:
                    hotels = hotels.order_by(sort_field)

            if "limit" in filters:
                i = int(filters["limit"])
                assert isinstance(i, int)
                try:
                    limit = int(filters["limit"])
                    hotels = hotels[:limit]
                except ValueError:
                    pass  # Ignorar si el límite no es un número válido

        return hotels

    # Others -----------------------------------------------------------------

    @staticmethod
    def get_all_room_types_of_hotel(hotel_id):
        return RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)

    @staticmethod
    def get_total_vacancy_for_each_room_type_of_hotel(pk):
        room_types = HotelService.get_all_room_types_of_hotel(pk)
        vacancy_data = []

        for room_type in room_types:
            num_rooms = Room.objects.filter(room_type=room_type).count()
            total_vacancy = room_type.capacity * num_rooms
            vacancy_data.append(
                {"room_type_id": room_type.id, "total_vacancy": total_vacancy}
            )

        return vacancy_data
