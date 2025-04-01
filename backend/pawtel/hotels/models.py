from django.db import models
from django.utils.translation import gettext_lazy as _
from pawtel.hotel_owners.models import HotelOwner


class Hotel(models.Model):

    # Attributes -------------------------------------------------------------

    is_archived = models.BooleanField(default=False, null=False)

    name = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            "unique": _("El nombre del hotel ya está en uso. Por favor, elige otro."),
        },
        blank=False,
        null=False,
    )

    address = models.CharField(max_length=100, blank=False, null=False)

    city = models.CharField(max_length=50, blank=False, null=False)

    description = models.CharField(max_length=400, blank=False, null=False)

    # Relations --------------------------------------------------------------

    hotel_owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"Hotel {self.name}, {self.city}"


class HotelImage(models.Model):
    image = models.ImageField(upload_to="hotels/", blank=False, null=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    is_cover = models.BooleanField(default=False, null=False)
