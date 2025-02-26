from rest_framework import serializers
from hotelOwners.models import HotelOwner

class HotelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwner  # Usamos el modelo HotelOwner
        fields = [
            "id", "username", "first_name", "last_name", "email", "phone",
            "date_joined", "last_login", "is_active", "is_staff", "is_superuser"
        ]
        extra_kwargs = {
            "email": {"required": True},
            "phone": {"required": True},
        }

    def to_representation(self, instance):
        """Convierte los nombres de los campos a snake case en la salida JSON"""
        representation = super().to_representation(instance)  # Obtiene representación estándar

        return {
            "id": representation["id"],
            "username": representation["username"],
            "first_name": representation["first_name"],  # first_name → firstName
            "last_name": representation["last_name"],  # last_name → lastName
            "email": representation["email"],
            "phone": representation["phone"],
            "date_joined": representation["date_joined"],  # date_joined → dateJoined
            "last_login": representation["last_login"],  # last_login → lastLogin
            "is_active": representation["is_active"],  # is_active → isActive
            "is_staff": representation["is_staff"],  # is_staff → isStaff
            "is_superuser": representation["is_superuser"],  # is_superuser → isSuperuser
        }

        #realmente este serializador no cambia nada ya que los atributos de la clase AbstractUser ya vienen en snake_case pero
        #lo hago ya que se quedo que habría un serializador por entidad