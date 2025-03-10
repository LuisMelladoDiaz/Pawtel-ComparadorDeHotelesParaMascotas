from django.db import models
from pawtel.app_users.models import AppUser


class HotelOwner(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}"
