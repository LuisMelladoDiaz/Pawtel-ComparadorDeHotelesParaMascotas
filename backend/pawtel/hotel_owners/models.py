from django.db import models
from pawtel.app_users.models import AppUser


class HotelOwner(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.user.username}"
