from pawtel.app_users.serializers import AppUserSerializer
from pawtel.base_serializer import BaseSerializer
from pawtel.hotel_owners.models import HotelOwner


class HotelOwnerSerializer(BaseSerializer):

    fields_required_for_post = []
    fields_editable = []
    fields_not_readable = []

    user = AppUserSerializer(read_only=True)

    class Meta:
        model = HotelOwner
        fields = ["id", "user"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True, "allow_null": False},
        }
