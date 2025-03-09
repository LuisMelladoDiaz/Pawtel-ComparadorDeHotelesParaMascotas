from django.contrib.auth.models import AbstractUser, BaseUserManager
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

    groups = None
    user_permissions = None

    def __str__(self):
        return f"{self.username}"


class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
