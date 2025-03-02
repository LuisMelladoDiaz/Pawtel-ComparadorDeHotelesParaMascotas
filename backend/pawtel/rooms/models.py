from django.db import models
from pawtel.room_types.models import RoomType


class Room(models.Model):

    # Attributes -------------------------------------------------------------

    is_archived = models.BooleanField(default=False, null=False)

    name = models.CharField(max_length=50, blank=False, null=False)

    # Relations --------------------------------------------------------------

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"{self.name} ({self.room_type.name})"
