from django.db import models
from django.core.validators import MinLengthValidator
from hotelOwners.models import HotelOwner

class Hotel(models.Model):
    hotel_owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=300, blank=False, null=False)

    def __str__(self):
        return f"Hotel {self.name}, {self.city}"