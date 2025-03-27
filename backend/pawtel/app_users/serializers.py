from rest_framework import serializers
from pawtel.app_users.models import AppUser, TermsAcceptance
from pawtel.base_serializer import BaseSerializer
from pawtel.utils import get_client_ip  


class AppUserSerializer(BaseSerializer):

    fields_required_for_post = ["username", "email", "phone", "password", "accept_terms"]
    fields_editable = ["username", "email", "phone", "password"]
    fields_not_readable = ["password"]

    accept_terms = serializers.BooleanField(write_only=True) 

    class Meta:
        model = AppUser
        fields = [
            "id",
            "username",
            "password",
            "email",
            "phone",
            "date_joined",
            "last_login",
            "is_active",
            "accept_terms",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "username": {"allow_null": False},
            "email": {"max_length": 100, "allow_null": False},
            "phone": {
                "max_length": 13,
                "validators": [AppUser.phone_regex],
                "allow_null": False,
            },
            "date_joined": {"read_only": True},
            "last_login": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")  
        accept_terms = validated_data.pop("accept_terms", False)

        if not accept_terms:
            raise serializers.ValidationError({"accept_terms": "Debes aceptar los términos y condiciones"})

        password = validated_data.pop("password")
        user = AppUser(**validated_data)
        user.set_password(password)
        user.save()

        
        TermsAcceptance.objects.create(
            user=user,
            terms_version="1.0",  
            ip_address=get_client_ip(request)
        )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
