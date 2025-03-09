from django.db import models
from pawtel.app_users.models import AppUser


class HotelOwner(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}"

    @staticmethod
    def create_hotel_owner(email: str, username: str, password: str, phone: str):
        user = AppUser.objects.create_user(
            email=email, username=username, password=password, phone=phone
        )
        hotel_owner = HotelOwner.objects.create(user=user)
        return hotel_owner
