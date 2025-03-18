from django.db.models import Max, Min
from pawtel.base_serializer import BaseSerializer
from pawtel.hotels.models import Hotel, HotelImage
from pawtel.room_types.models import RoomType
from rest_framework import serializers


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ["id", "image", "is_cover", "hotel"]


class HotelSerializer(BaseSerializer):
    fields_required_for_post = ["name", "address", "city", "description", "hotel_owner"]
    fields_editable = ["name", "address", "city", "description"]
    fields_not_readable = []

    cheapest_price = serializers.SerializerMethodField()
    most_expensive_price = serializers.SerializerMethodField()
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
            "cheapest_price",
            "most_expensive_price",
            "images",
            "cover_image",
        ]

    def get_cheapest_price(self, obj):
        cheapest = RoomType.objects.filter(hotel=obj).aggregate(
            min_price=Min("price_per_night")
        )["min_price"]
        return cheapest if cheapest is not None else None

    def get_most_expensive_price(self, obj):
        most_expensive = RoomType.objects.filter(hotel=obj).aggregate(
            max_price=Max("price_per_night")
        )["max_price"]
        return most_expensive if most_expensive is not None else None

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
