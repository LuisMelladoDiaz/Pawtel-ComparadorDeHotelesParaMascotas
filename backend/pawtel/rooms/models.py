from django.db import models
from django.core.validators import MinLengthValidator
from roomTypes.models import RoomType  # Importamos RoomType

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False)

    def __str__(self):
        return f"{self.name} ({self.room_type.name})"