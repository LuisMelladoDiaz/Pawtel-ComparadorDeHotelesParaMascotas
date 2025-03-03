from rest_framework import serializers
from pawtel.appUsers.models import AppUser
from pawtel.hotelOwners.models import HotelOwner


class HotelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwner  
        fields = [
            "id", "username", "first_name", "last_name", "email", "phone",
            "date_joined", "last_login", "is_active", "is_staff", "is_superuser"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "username": {"allow_null": False, "required": True},
            "email": {"required": True, "max_length": 100, "allow_null": False},
            "phone": {"required": True, "max_length": 13, "validators": [AppUser.phone_regex], "allow_null": False},
        }

