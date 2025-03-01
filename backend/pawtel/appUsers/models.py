from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator


class AppUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+34\d{9}$',
        message="Phone number must be in the format: +34XXXXXXXXX"
    )
    
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, max_length=100, null=False)
    
    # Fix conflicts with auth.User groups and permissions
    groups = models.ManyToManyField(Group, related_name="appusers_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="appusers_permissions", blank=True)


    def __str__(self):
        return f"{self.username}"