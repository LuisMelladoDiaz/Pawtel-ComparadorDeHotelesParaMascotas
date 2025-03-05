from pawtel.app_users.models import AppUser


class HotelOwner(AppUser):

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"{self.username}"
