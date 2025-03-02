from django.core.validators import MinValueValidator
from django.db import models
from pawtel.hotels.models import Hotel


class PetType(models.TextChoices):
    DOG = "DOG", "Dog"
    CAT = "CAT", "Cat"
    BIRD = "BIRD", "Bird"
    ANY = "ANY", "Any"


class RoomType(models.Model):

    is_archived = models.BooleanField(default=False, null=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=300, blank=False, null=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], null=False)
    price_per_night = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=False
    )
    pet_type = models.CharField(
        max_length=10, choices=PetType.choices, default=PetType.ANY, null=False
    )

    def __str__(self):
        return f"{self.name} ({self.hotel.name})"
