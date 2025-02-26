from rest_framework import serializers
from hotels.models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel  # Especificamos el modelo Hotel
        fields = [
            "id", "name", "address", "city", "description"
        ]
        extra_kwargs = {
            "name": {"required": True},
            "address": {"required": True},
            "city": {"required": True},
            "description": {"required": True},
        }

    def to_representation(self, instance):
        """Convierte los nombres de los campos a snake_case en la salida JSON"""
        representation = super().to_representation(instance)  

        return {
            "id": representation["id"],
            "name": representation["name"],
            "address": representation["address"],
            "city": representation["city"],
            "description": representation["description"]
        }
