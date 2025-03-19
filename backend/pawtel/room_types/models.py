from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pawtel.hotels.models import Hotel


class PetType(models.TextChoices):
    DOG = "DOG", "Dog"
    CAT = "CAT", "Cat"
    BIRD = "BIRD", "Bird"
    MIXED = "MIXED", "Mixed"


class RoomType(models.Model):

    # Attributes -------------------------------------------------------------

    is_archived = models.BooleanField(default=False, null=False)

    name = models.CharField(max_length=50, blank=False, null=False)

    description = models.CharField(max_length=300, blank=False, null=False)

    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(200)], null=False
    )

    num_rooms = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)], null=False
    )

    price_per_night = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=False
    )

    pet_type = models.CharField(
        max_length=30, choices=PetType.choices, blank=False, null=False
    )

    # Relations --------------------------------------------------------------

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"{self.name} ({self.hotel.name})"
