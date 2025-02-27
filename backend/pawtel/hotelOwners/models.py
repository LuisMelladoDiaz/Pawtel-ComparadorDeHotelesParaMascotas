from django.db import models
from accounts.models import AppUser  

class HotelOwner(AppUser):
    def __str__(self):
        return f"{self.username}"