from django.db.models import Max, Min
from pawtel.base_serializer import BaseSerializer
from pawtel.hotels.models import Hotel, HotelImage
from pawtel.room_types.models import RoomType
from rest_framework import serializers


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ["id", "image", "is_cover", "hotel"]


class SetImageAsCoverSerializer(serializers.Serializer):
    is_cover = serializers.BooleanField(required=True, allow_null=False)


class HotelSerializer(BaseSerializer):
    fields_required_for_post = ["name", "address", "city", "description", "hotel_owner"]
    fields_editable = ["name", "address", "city", "description"]
    fields_not_readable = []

    lowest_price_current_filters = serializers.SerializerMethodField()
    highest_price_current_filters = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            "id",
            "is_archived",
            "name",
            "address",
            "city",
            "description",
            "hotel_owner",
            "lowest_price_current_filters",
            "highest_price_current_filters",
            "images",
            "cover_image",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_archived": {"read_only": True},
            "name": {"max_length": 100, "allow_null": False},
            "address": {"max_length": 100, "allow_null": False},
            "city": {"max_length": 50, "allow_null": False},
            "description": {"max_length": 400, "allow_null": False},
            "hotel_owner": {"allow_null": False},
        }

    def get_lowest_price_current_filters(self, obj):
        min_price_filters = getattr(obj, "min_price_filters", None)

        if min_price_filters is not None:  # computed by annotate in filter
            return min_price_filters
        else:
            lowest_price = RoomType.objects.filter(hotel=obj).aggregate(
                min_price=Min("price_per_night")
            )["min_price"]
            return lowest_price if lowest_price is not None else None

    def get_highest_price_current_filters(self, obj):
        max_price_filters = getattr(obj, "max_price_filters", None)

        if max_price_filters is not None:  # computed by annotate in filter
            return max_price_filters
        else:
            highest_price = RoomType.objects.filter(hotel=obj).aggregate(
                max_price=Max("price_per_night")
            )["max_price"]
            return highest_price if highest_price is not None else None

    def get_images(self, obj):
        images = obj.images.all()
        return HotelImageSerializer(images, many=True, context=self.context).data

    def get_cover_image(self, obj):
        cover_image = obj.images.filter(is_cover=True).first()
        return (
            HotelImageSerializer(cover_image, context=self.context).data
            if cover_image
            else None
        )
