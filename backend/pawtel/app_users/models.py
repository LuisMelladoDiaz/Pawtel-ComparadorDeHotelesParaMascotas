from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models


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

    # Fix conflicts with auth.User groups
    groups = models.ManyToManyField(Group, related_name="appusers_groups", blank=True)

    # Fix conflicts with auth.User permissions
    user_permissions = models.ManyToManyField(
        Permission, related_name="appusers_permissions", blank=True
    )

    # is_active is by default True, is_staff is by default False, and is_superuser is by default False.

    # Meta configuration -----------------------------------------------------

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.username}"
