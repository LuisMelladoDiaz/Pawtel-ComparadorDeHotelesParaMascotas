from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pawtel.app_users.models import AppUser


class Customer(models.Model):

    # Attributes -------------------------------------------------------------

    paw_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        null=False,
    )

    # Relations --------------------------------------------------------------

    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, null=False, related_name="customer"
    )

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"{self.user.username}"
