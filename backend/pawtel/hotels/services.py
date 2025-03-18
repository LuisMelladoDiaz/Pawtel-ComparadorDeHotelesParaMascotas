from django.db.models import Max, Min
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel
from pawtel.hotels.serializers import HotelSerializer
from pawtel.room_types.models import RoomType
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class HotelService:

    @staticmethod
    def check_permission(user, action):
        """Checks if the user has permission to perform an action based on their type."""

        customer_permissions = {
            "allowed_actions": ["list", "retrieve", "get_all_room_types_of_hotel"],
            "denied_actions": ["create", "update", "destroy", "get_bookings_of_hotel"],
        }

        hotel_owner_permissions = {
            "allowed_actions": [
                "list",
                "retrieve",
                "create",
                "update",
                "destroy",
                "get_all_room_types_of_hotel",
                "get_bookings_of_hotel",
            ],
            "denied_actions": [],
        }

        """
        app_admin_permissions = {
            'allowed_actions': [
                'list', 'retrieve',
                'get_all_room_types_of_hotel', 'get_bookings_of_hotel'
            ],
            'denied_actions': ['create','update', 'destroy']
        }
        """

        if hasattr(user, "customer"):
            permissions = customer_permissions
            user_type = "Customer"
        elif hasattr(user, "hotel_owner"):
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

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_hotel(request, pk, permission_granted):
        if permission_granted:
            hotel = HotelService.retrieve_hotel(pk, permission_granted, None)
            hotel_owner = HotelOwnerService.get_current_hotel_owner(
                request, permission_granted
            )

            if (not hotel) or (hotel.is_archived):
                raise NotFound("Hotel does not exist.")

            if hotel.hotel_owner.id != hotel_owner.id:
                raise PermissionDenied("Permission denied.")

    @staticmethod
    def serialize_output_hotel(hotel, many=False):
        return HotelSerializer(hotel, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel(pk, permission_granted, user_type):
        if permission_granted:
            # if not user_type == "AppAdmin":
            try:
                hotel = Hotel.objects.get(pk=pk)
                if hotel.is_archived:
                    raise PermissionDenied("")
                return hotel
            except Hotel.DoesNotExist:
                raise NotFound(detail=f"Hotel with id {pk} not found")
            """
             else:
                try:
                    return  Hotel.objects.get(pk=pk)
                except Hotel.DoesNotExist:
                    raise NotFound(detail=f"Hotel with id {pk} not found")
            """

    # POST -------------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_create(request):
        context = {"request": request}
        current_owner_id = HotelOwnerService.get_current_hotel_owner(request, True).id
        data = request.data.copy()
        data["hotel_owner"] = current_owner_id
        serializer = HotelSerializer(data=data, context=context)
        return serializer

    @staticmethod
    def validate_create_hotel(input_serializer, permission_granted):
        if permission_granted:
            if not input_serializer.is_valid():
                raise ValidationError(input_serializer.errors)

            name = input_serializer.validated_data.get("name")
            hotel_owner_id = input_serializer.validated_data.get("hotel_owner").id

            if not HotelOwnerService.retrieve_hotel_owner(
                hotel_owner_id
            ).user.is_active:
                raise ValidationError({"hotel_owner": "Invalid hotel owner."})

            if name and Hotel.objects.filter(name=name).exists():
                raise ValidationError({"name": "Name in use."})

    @staticmethod
    def create_hotel(input_serializer):
        hotel_created = input_serializer.save()
        return hotel_created

    # PUT/PATCH --------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_update(request, pk, permission_granted):
        hotel = HotelService.retrieve_hotel(pk, permission_granted, None)
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
    def update_hotel(pk, input_serializer, permission_granted):
        hotel = HotelService.retrieve_hotel(pk, permission_granted, None)
        return input_serializer.update(hotel, input_serializer.validated_data)

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_hotel(pk, permission_granted):
        hotel = HotelService.retrieve_hotel(pk, permission_granted, None)
        hotel.delete()

    # Filter -----------------------------------------------------------------

    @staticmethod
    def list_hotels(filters=None, permission_granted=None, user_type=None):
        if permission_granted:
            # if not user_type == "AppAdmin":
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
                            roomtype__price_per_night__gte=min_price
                        ).distinct()
                    except ValueError:
                        pass

                hotels = hotels.annotate(
                    price_max=Max("roomtype__price_per_night"),
                    price_min=Min("roomtype__price_per_night"),
                )
                if "sort_by" in filters:
                    assert isinstance(filters["sort_by"], str)

                    valid = [
                        "price_per_night",
                        "city",
                        "name",
                        "price_max",
                        "price_min",
                    ]
                    # Verificamos si sort_by está en los campos válidos o si empieza con "-"
                    assert filters["sort_by"] in valid or filters["sort_by"].startswith(
                        "-"
                    )

                    sort_field = filters["sort_by"]

                    # Si el campo comienza con "-", orden descendente
                    if sort_field.startswith("-"):
                        hotels = hotels.order_by(sort_field)  # Orden descendente
                    else:
                        hotels = hotels.order_by(sort_field)  # Orden ascendente

                if "limit" in filters:
                    i = int(filters["limit"])
                    assert isinstance(i, int)
                    try:
                        limit = int(filters["limit"])
                        hotels = hotels[:limit]
                    except ValueError:
                        pass  # Ignorar si el límite no es un número válido
        """ else:
                hotels = Hotel.objects.all()"
            """
        return hotels

    # Others -----------------------------------------------------------------

    @staticmethod
    def get_all_room_types_of_hotel(hotel_id):
        return RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)
