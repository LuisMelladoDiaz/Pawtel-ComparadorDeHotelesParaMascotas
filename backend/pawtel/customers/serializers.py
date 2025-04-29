from pawtel.app_users.serializers import AppUserSerializer
from pawtel.base_serializer import BaseSerializer
from pawtel.customers.models import Customer


class CustomerSerializer(BaseSerializer):

    fields_required_for_post = ["paw_points"]
    fields_editable = ["paw_points"]
    fields_not_readable = []

    user = AppUserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "paw_points", "user"]
        extra_kwargs = {
            "id": {"read_only": True},
            "paw_points": {"min_value": 0, "max_value": 200, "allow_null": False},
            "user": {"read_only": True, "allow_null": False},
        }
