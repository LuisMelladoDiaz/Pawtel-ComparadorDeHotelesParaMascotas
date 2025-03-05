from django.db import models
from pawtel.hotel_owners.models import HotelOwner


class Hotel(models.Model):

    # Attributes -------------------------------------------------------------

    is_archived = models.BooleanField(default=False, null=False)

    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    address = models.CharField(max_length=100, blank=False, null=False)

    city = models.CharField(max_length=50, blank=False, null=False)

    description = models.CharField(max_length=300, blank=False, null=False)

    # Relations --------------------------------------------------------------

    hotel_owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"Hotel {self.name}, {self.city}"
