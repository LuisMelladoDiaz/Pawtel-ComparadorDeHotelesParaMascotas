from django.db import models
from pawtel.app_users.models import AppUser


class Customer(models.Model):
    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, null=False, related_name="customer"
    )

    def __str__(self):
        return f"{self.user.username}"
