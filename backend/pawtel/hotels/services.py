from datetime import date, datetime, timedelta

from django.db.models import Max, Min, Q
from django.forms import ValidationError
from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.bookings.models import Booking
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel, HotelImage
from pawtel.hotels.serializers import (HotelImageSerializer, HotelSerializer,
                                       SetImageAsCoverSerializer)
from pawtel.permission_services import PermissionService
from pawtel.room_types.models import RoomType
from pawtel.room_types.services import RoomTypeService
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class HotelService:

    THREE_YEARS = timedelta(days=3 * 365)

    # -
    # -------------------------------------------------------------------------
    # Hotels ------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # -

    # Authorization ----------------------------------------------------------

    def authorize_action_hotel_level_1(request, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_hotel_service(role_user, action_name)
        return role_user

    def authorize_action_hotel_level_2(request, hotel_id, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_hotel_service(role_user, action_name)
        HotelService.retrieve_hotel(hotel_id)
        return role_user

    def authorize_action_hotel_level_3(request, hotel_id, action_name):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_hotel_service(role_user, action_name)
        hotel = HotelService.retrieve_hotel(hotel_id)
        HotelService.check_ownership_hotel(role_user, hotel)
        return role_user

    def check_ownership_hotel(role_user, hotel):
        if role_user.user.role == UserRole.ADMIN:
            return

        elif role_user.user.role == UserRole.HOTEL_OWNER:
            if hotel.hotel_owner.id != role_user.id:
                raise PermissionDenied("Permission denied.")

        else:
            raise PermissionDenied("Permission denied.")

    # Serialization ----------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_create(request):
        context = {"request": request}
        current_owner_id = HotelOwnerService.get_current_hotel_owner(request).id
        data = request.data.copy()
        data["hotel_owner"] = current_owner_id
        serializer = HotelSerializer(data=data, context=context)
        return serializer

    @staticmethod
    def serialize_input_hotel_update(request, pk):
        hotel = HotelService.retrieve_hotel(pk)
        context = {"request": request}
        serializer = HotelSerializer(instance=hotel, data=request.data, context=context)
        return serializer

    @staticmethod
    def serialize_output_hotel(hotel, many=False, context=None):
        return HotelSerializer(hotel, many=many, context=context).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel(pk, allow_archived=False):
        try:
            if allow_archived:
                return Hotel.objects.get(pk=pk)
            else:
                return Hotel.objects.get(pk=pk, is_archived=False)
        except Hotel.DoesNotExist:
            raise NotFound(detail="Hotel not found.")

    @staticmethod
    def list_bookings_of_hotel(hotel_id):
        return Booking.objects.filter(room_type__hotel=hotel_id)

    # POST -------------------------------------------------------------------

    @staticmethod
    def validate_create_hotel(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        name = input_serializer.validated_data.get("name")
        if name and Hotel.objects.filter(name=name).exists():
            raise ValidationError({"name": "Name in use."})

    @staticmethod
    def create_hotel(input_serializer):
        hotel_created = input_serializer.save()
        return hotel_created

    # PUT/PATCH --------------------------------------------------------------

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

    @staticmethod
    def validate_all_room_types_deletion(hotel_pk):
        hotel = Hotel.objects.get(pk=hotel_pk)
        room_types = RoomType.objects.filter(hotel=hotel)
        today = date.today()
        delete = True

        for room_type in room_types:
            past_limit = today - HotelService.THREE_YEARS

            recent_bookings = Booking.objects.filter(
                room_type_id=room_type.id, start_date__range=(past_limit, today)
            )
            future_bookings = Booking.objects.filter(
                room_type_id=room_type.id, start_date__gte=today
            )

            if future_bookings.exists():
                raise ValidationError(
                    {
                        "detail": "Object cannot be deleted because there is an upcoming booking."
                    }
                )

            if recent_bookings.exists():
                delete = False
                break

        return delete

    def archive_hotel(hotel_id):
        RoomType.objects.filter(hotel_id=hotel_id).update(is_archived=True)
        Hotel.objects.filter(pk=hotel_id).update(is_archived=True)

    # Filter -----------------------------------------------------------------

    VALID_FILTERS = {
        "city": str,
        "name": str,
        "hotel_owner": int,
        "pet_type": str,
        "max_price_per_night": float,
        "min_price_per_night": float,
        "sort_by": str,
        "limit": int,
        "start_date": lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        "end_date": lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        "is_available": lambda v: str(v).lower() in ("true", "1"),  # If true or 1, True
    }

    @staticmethod
    def __validate_filters(filters):
        """Ensures filters are valid and have correct types."""
        if filters is None:
            return {}

        assert all(
            f in HotelService.VALID_FILTERS for f in filters
        ), f"Invalid filter: {filters}"

        validated = {}
        for key, expected_type in HotelService.VALID_FILTERS.items():
            if key in filters:
                try:
                    validated[key] = expected_type(filters[key])
                except (ValueError, TypeError):
                    pass
        return validated

    @staticmethod
    def is_hotel_available(
        hotel_id, start_date, end_date, pet_type=None, min_price=None, max_price=None
    ):
        room_types = HotelService.get_all_room_types_of_hotel(hotel_id)
        for room_type in room_types:
            if pet_type and room_type.pet_type != pet_type:
                continue
            if min_price and room_type.price_per_night < min_price:
                continue
            if max_price and room_type.price_per_night > max_price:
                continue
            if RoomTypeService.is_room_type_available(
                room_type.id, start_date, end_date
            ):
                return True

        return False

    @staticmethod
    def __apply_filters(hotels, filters):
        """Applies filters to a queryset."""
        q = Q()

        if "city" in filters:
            q &= Q(city__icontains=filters["city"])

        if "name" in filters:
            q &= Q(name__icontains=filters["name"])

        if "hotel_owner" in filters:
            q &= Q(hotel_owner__id=filters["hotel_owner"])

        if "pet_type" in filters:
            q &= Q(roomtype__pet_type=filters["pet_type"], roomtype__is_archived=False)

        if "max_price_per_night" in filters:
            q &= Q(roomtype__price_per_night__lte=filters["max_price_per_night"])

        if "min_price_per_night" in filters:
            q &= Q(roomtype__price_per_night__gte=filters["min_price_per_night"])

        filtered_hotels = hotels.filter(q).distinct()

        if (
            ("is_available" in filters)
            and ("start_date" in filters)
            and ("end_date" in filters)
            and filters.get("is_available") is True
        ):
            start_date = filters.get("start_date")
            end_date = filters.get("end_date")
            RoomTypeService.validate_room_type_is_available(start_date, end_date)

            available_hotel_ids = [
                hotel.id
                for hotel in filtered_hotels
                if HotelService.is_hotel_available(
                    hotel.id,
                    start_date,
                    end_date,
                    filters.get("pet_type"),
                    filters.get("min_price_per_night"),
                    filters.get("max_price_per_night"),
                )
            ]

            filtered_hotels = filtered_hotels.filter(
                id__in=available_hotel_ids
            ).distinct()

        return filtered_hotels.annotate(
            price_max=Max("roomtype__price_per_night"),
            price_min=Min("roomtype__price_per_night"),
        )

    @staticmethod
    def list_filtered_hotels(filters=None, allow_archived=False):
        """Lists hotels with filtering, sorting, and limiting."""
        if allow_archived:
            hotels = Hotel.objects.all()
        else:
            hotels = Hotel.objects.filter(is_archived=False)

        filters = HotelService.__validate_filters(filters)
        hotels = HotelService.__apply_filters(hotels, filters)

        if "sort_by" in filters:
            sort_field = filters["sort_by"]
            valid_sort_fields = [
                "price_per_night",
                "city",
                "name",
                "price_max",
                "price_min",
            ]
            assert (
                sort_field.lstrip("-") in valid_sort_fields
            ), f"Invalid sort field: {sort_field}"
            hotels = hotels.order_by(sort_field)

        if "limit" in filters:
            hotels = hotels[: filters["limit"]]

        return hotels

    # Others -----------------------------------------------------------------

    @staticmethod
    def list_room_types_of_hotel(hotel_id):
        return RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)

    @staticmethod
    def get_all_room_types_of_hotel(hotel_id):
        return RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)

    # -
    # -------------------------------------------------------------------------
    # HotelImages -------------------------------------------------------------
    # -------------------------------------------------------------------------
    # -

    # Serialization ----------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_image(request, hotel_id):
        context = {"request": request}
        hotel = HotelService.retrieve_hotel(hotel_id)
        data = request.data.copy()
        data["hotel"] = hotel.id
        serializer = HotelImageSerializer(data=data, context=context)
        return serializer

    @staticmethod
    def serialize_output_hotel_image(hotel_image, many=False, context=None):
        return HotelImageSerializer(hotel_image, many=many, context=context).data

    @staticmethod
    def serialize_input_set_image_is_cover(request):
        context = {"request": request}
        data = request.data.copy()
        serializer = SetImageAsCoverSerializer(data=data, context=context)
        return serializer

    # Validation -------------------------------------------------------------

    def validate_upload_image(input_serializer, hotel_id):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        hotel = HotelService.retrieve_hotel(hotel_id)
        if hotel.images.count() >= 5:
            raise ValidationError({"hotel": "A hotel cannot have more than 5 images."})

    @staticmethod
    def validate_update_image(input_serializer, hotel_id, image_id):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        ##! Should better go in an authorize
        HotelService.retrieve_image_from_hotel(hotel_id, image_id)

    @staticmethod
    def validate_set_image_is_cover(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

    # GET --------------------------------------------------------------------

    @staticmethod
    def list_images_of_hotel(hotel_id):
        return HotelImage.objects.filter(hotel_id=hotel_id)

    @staticmethod
    def retrieve_image_from_hotel(hotel_id, image_id):
        try:
            return HotelImage.objects.get(id=image_id, hotel_id=hotel_id)
        except HotelImage.DoesNotExist:
            raise NotFound(detail="Hotel Image not found.")

    @staticmethod
    def retrieve_current_cover_image_or_404(hotel_id):
        try:
            cover_image = HotelImage.objects.get(hotel__id=hotel_id, is_cover=True)
            return cover_image
        except HotelImage.DoesNotExist:
            raise NotFound(detail="No cover image found for the hotel.")

    @staticmethod
    def retrieve_current_cover_image(hotel_id):
        cover_image = HotelImage.objects.filter(
            hotel__id=hotel_id, is_cover=True
        ).first()
        return cover_image

    @staticmethod
    def list_non_cover_images(hotel_id):
        hotel_images = HotelImage.objects.filter(hotel__id=hotel_id, is_cover=False)
        return hotel_images

    # POST -------------------------------------------------------------------

    @staticmethod
    def upload_image_to_hotel(input_serializer):
        hotel = input_serializer.validated_data["hotel"]
        current_image_count = hotel.images.count()

        if current_image_count == 0:
            input_serializer.validated_data["is_cover"] = True

        if input_serializer.validated_data.get("is_cover", False):
            current_cover_image = HotelService.retrieve_current_cover_image(hotel.id)
            if current_cover_image:
                current_cover_image.is_cover = False
                current_cover_image.save()

        hotel_image_created = input_serializer.save()
        return hotel_image_created

    # PUT/PATCH --------------------------------------------------------------

    @staticmethod
    def update_image_to_hotel(input_serializer, hotel_id, image_id):
        hotel = input_serializer.validated_data["hotel"]
        current_image_count = hotel.images.count()

        hotel_image = HotelService.retrieve_image_from_hotel(hotel_id, image_id)

        if input_serializer.validated_data.get("is_cover", False):
            current_cover_image = HotelService.retrieve_current_cover_image(hotel_id)
            if current_cover_image and current_cover_image != hotel_image:
                current_cover_image.is_cover = False
                current_cover_image.save()

        return input_serializer.update(hotel_image, input_serializer.validated_data)

    @staticmethod
    def set_image_is_cover(input_serializer, hotel_id, image_id):
        hotel = HotelService.retrieve_hotel(hotel_id)
        hotel_image = HotelService.retrieve_image_from_hotel(hotel_id, image_id)
        if input_serializer.validated_data.get("is_cover"):
            current_cover_image = HotelService.retrieve_current_cover_image(hotel_id)
            if current_cover_image and current_cover_image.id != image_id:
                current_cover_image.is_cover = False
                current_cover_image.save()

            if not hotel_image.is_cover:
                hotel_image.is_cover = True
                hotel_image.save()

        else:
            current_image_count = hotel.images.count()
            if current_image_count <= 5 and hotel_image.is_cover:
                hotel_image.is_cover = False
                hotel_image.save()

        return hotel_image

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_image_from_hotel(hotel_id, image_id):
        hotel_image = HotelService.retrieve_image_from_hotel(hotel_id, image_id)
        hotel_image.delete()
