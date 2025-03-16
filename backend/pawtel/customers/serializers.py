from pawtel.app_users.serializers import AppUserSerializer
from pawtel.base_serializer import BaseSerializer
from pawtel.customers.models import Customer


class CustomerSerializer(BaseSerializer):

    fields_required_for_post = []
    fields_editable = []
    fields_not_readable = []

    user = AppUserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True, "allow_null": False},
        }
