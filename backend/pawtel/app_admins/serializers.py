from pawtel.app_admins.models import App_Admin
from pawtel.app_users.serializers import AppUserSerializer
from pawtel.base_serializer import BaseSerializer


class AdminSerializer(BaseSerializer):
    fields_required_for_post = []
    fields_editable = []
    fields_not_readable = []

    user = AppUserSerializer(read_only=True)

    class Meta:
        model = App_Admin
        fields = ["id", "user"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True, "allow_null": False},
        }
