from django.db.models import Max, Min
from django.forms import ValidationError
from pawtel.bookings.models import Booking
from pawtel.hotel_owners.services import HotelOwnerService
from pawtel.hotels.models import Hotel, HotelImage
from pawtel.hotels.serializers import HotelImageSerializer, HotelSerializer
from pawtel.room_types.models import RoomType
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class HotelService:

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_hotel(request, pk):
        hotel = HotelService.retrieve_hotel(pk)
        hotel_owner = HotelOwnerService.get_current_hotel_owner(request)

        if hotel.hotel_owner.id != hotel_owner.id:
            raise PermissionDenied("Permission denied.")

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

                valid = ["price_per_night", "city", "name", "price_max", "price_min"]
                # Verificamos si sort_by está en los campos válidos o si empieza con "-"
                assert filters["sort_by"] in valid or filters["sort_by"].startswith("-")

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

        return hotels

    # Others -----------------------------------------------------------------

    @staticmethod
    def list_room_types_of_hotel(hotel_id):
        return RoomType.objects.filter(hotel_id=hotel_id, is_archived=False)

    # Hotel_Image -------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_image(request, pk):
        context = {"request": request}
        hotel = HotelService.retrieve_hotel(pk)
        data = request.data.copy()
        data["hotel"] = hotel.id
        serializer = HotelImageSerializer(data=data, context=context)
        return serializer

    def validate_upload_image(input_serializer, pk):
        hotel = HotelService.retrieve_hotel(pk)
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)
        if hotel.images.count() >= 5:
            raise ValidationError({"hotel": "A hotel cannot have more than 5 images."})

    @staticmethod
    def upload_image_to_hotel(input_serializer):
        hotel = input_serializer.validated_data["hotel"]
        current_image_count = hotel.images.count()

        if current_image_count == 0:
            input_serializer.validated_data["is_cover"] = True

        if input_serializer.validated_data.get("is_cover", False):
            current_cover_image = HotelImage.objects.filter(
                hotel=hotel, is_cover=True
            ).first()

            if current_cover_image:
                current_cover_image.is_cover = False
                current_cover_image.save()

        hotel_image_created = input_serializer.save()
        return hotel_image_created

    @staticmethod
    def serialize_output_hotel_image(hotel_image, many=False, context=None):
        return HotelImageSerializer(hotel_image, many=many, context=context).data

    @staticmethod
    def retrieve_image_from_hotel(hotel_id, image_id):
        try:
            return HotelImage.objects.get(id=image_id, hotel_id=hotel_id)
        except HotelImage.DoesNotExist:
            raise NotFound(detail="Hotel Image not found.")

    @staticmethod
    def list_images_of_hotel(pk):
        hotel_images = HotelImage.objects.filter(hotel_id=pk)
        if not hotel_images:
            raise NotFound(detail="No images found for hotel.")
        return hotel_images

    @staticmethod
    def validate_update_image(input_serializer, pk, image_id):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        HotelService.retrieve_hotel(pk)  ##! TODO: Put this in authorize
        hotel_image = HotelService.retrieve_image_from_hotel(pk, image_id)

        if not hotel_image:
            raise NotFound(detail="Image not found or does not belong to the hotel.")

    @staticmethod
    def update_image_to_hotel(input_serializer, pk, image_id):
        hotel = input_serializer.validated_data["hotel"]
        current_image_count = hotel.images.count()

        hotel_image = HotelService.retrieve_image_from_hotel(pk, image_id)
        if current_image_count == 1:
            input_serializer.validated_data["is_cover"] = True

        if input_serializer.validated_data.get("is_cover", False):
            current_cover_image = HotelImage.objects.filter(
                hotel=hotel, is_cover=True
            ).first()

            if current_cover_image and current_cover_image != hotel_image:
                current_cover_image.is_cover = False
                current_cover_image.save()

        return input_serializer.update(hotel_image, input_serializer.validated_data)

    @staticmethod
    def delete_image_from_hotel(pk, image_id):
        hotel_image = HotelService.retrieve_image_from_hotel(pk, image_id)
        hotel_image.delete()

    @staticmethod
    def retrieve_cover_image(pk):
        try:
            hotel_image = HotelImage.objects.get(hotel__id=pk, is_cover=True)
        except HotelImage.DoesNotExist:
            raise NotFound(detail="No cover image found for the hotel.")
        return hotel_image

    @staticmethod
    def list_non_cover_images(pk):
        hotel_images = HotelImage.objects.filter(hotel__id=pk, is_cover=False)
        return hotel_images

    @staticmethod
    def validate_set_image_as_cover(pk, image_id):
        HotelService.retrieve_hotel(pk)  ##! TODO: Put this in authorize
        hotel_image = HotelService.retrieve_image_from_hotel(pk, image_id)

        if not hotel_image:
            raise NotFound(detail="Image not found or does not belong to the hotel.")

    @staticmethod
    def set_image_as_cover(pk, image_id):
        hotel_image = HotelService.retrieve_image_from_hotel(pk, image_id)
        current_cover_image = HotelImage.objects.filter(
            hotel__id=pk, is_cover=True
        ).first()

        if current_cover_image:
            current_cover_image.is_cover = False
            current_cover_image.save()

        hotel_image.is_cover = True
        hotel_image.save()

        return hotel_image
