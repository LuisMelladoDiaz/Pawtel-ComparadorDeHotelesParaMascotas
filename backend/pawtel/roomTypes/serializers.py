from rest_framework import serializers
from roomTypes.models import RoomType
from hotels.models import Hotel  # Importamos Hotel porque RoomType tiene una ForeignKey a Hotel

class RoomTypeSerializer(serializers.ModelSerializer):
    hotel = serializers.SlugRelatedField(    #Permite que en vez de devolver el ID del hotel en la fk, se muestre su nombre en JSON.
        queryset=Hotel.objects.all(),
        slug_field="name"     #Especifica que, en vez del ID, queremos que se muestre el campo name del hotel en el atributo del roomType.
    )

    class Meta:
        model = RoomType  # Especificamos el modelo RoomType
        fields = [
            "id", "name", "description", "capacity", "price_per_night", "pet_type", "hotel"
        ]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
            "capacity": {"required": True, "min_value": 1},
            "price_per_night": {"required": True, "min_value": 1.00},
            "pet_type": {"required": True},
            "hotel": {"required": True},
        }

    def to_representation(self, instance):
        """Convierte los nombres de los campos a snake_case en la salida JSON"""
        representation = super().to_representation(instance)  #representación default

        return {
            "id": representation["id"],
            "name": representation["name"],
            "description": representation["description"],
            "capacity": representation["capacity"],
            "price_per_night": representation["price_per_night"],
            "pet_type": representation["pet_type"],
            "hotel": representation["hotel"]  # Representa el nombre del hotel en vez del ID
        }
