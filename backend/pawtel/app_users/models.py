from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserRole(models.TextChoices):
    CUSTOMER = "CUSTOMER", "Customer"
    HOTEL_OWNER = "HOTEL_OWNER", "Hotel owner"
    ADMIN = "ADMIN", "Admin"
    INVALID = "INVALID", "Invalid"


class AppUser(AbstractUser):

    # Auxiliar ---------------------------------------------------------------

    phone_regex = RegexValidator(
        regex=r"^\+34\d{9}$", message="Phone number must be in the format: +34XXXXXXXXX"
    )

    # Attributes -------------------------------------------------------------

    phone = models.CharField(
        validators=[phone_regex], max_length=13, unique=True, blank=False, null=False
    )

    email = models.EmailField(unique=True, blank=False, max_length=100, null=False)

    groups = None
    user_permissions = None

    # Transient attributes ---------------------------------------------------

    @property
    def role(self):
        if hasattr(self, "customer"):
            return UserRole.CUSTOMER.value
        elif hasattr(self, "hotel_owner"):
            return UserRole.HOTEL_OWNER.value
        else:
            return UserRole.INVALID.value

    def __str__(self):
        return f"{self.username}"
