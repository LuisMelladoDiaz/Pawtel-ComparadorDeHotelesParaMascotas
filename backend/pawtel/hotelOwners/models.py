from django.db import models
from accounts.models import AppUser  # Importamos AppUser

class HotelOwner(AppUser):
    def __str__(self):
        return f"{self.username} (Hotel Owner)"