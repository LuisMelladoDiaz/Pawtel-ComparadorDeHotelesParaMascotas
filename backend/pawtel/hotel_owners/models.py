from django.db import models
from pawtel.app_users.models import AppUser


class HotelOwner(models.Model):
    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, null=False, related_name="hotel_owner"
    )
    is_approved = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f"{self.user.username}"
