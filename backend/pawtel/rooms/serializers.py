from rest_framework import serializers
from rooms.models import Room
from catalog.models import RoomType  # Importamos RoomType ya que es fk

class RoomSerializer(serializers.ModelSerializer):   #serializador para obtenerel nombre de la roomType en vez de id
    room_type = serializers.SlugRelatedField(
        queryset=RoomType.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Room  # Especificamos el modelo Room
        fields = [
            "id", "name", "room_type"
        ]
        extra_kwargs = {
            "name": {"required": True},
            "room_type": {"required": True},
        }

    def to_representation(self, instance):
        """Convierte los nombres de los campos a snake_case en la salida JSON"""
        representation = super().to_representation(instance)

        return {
            "id": representation["id"],
            "name": representation["name"],
            "room_type": representation["room_type"]  # Representa el nombre del tipo de habitación en vez de id
        }