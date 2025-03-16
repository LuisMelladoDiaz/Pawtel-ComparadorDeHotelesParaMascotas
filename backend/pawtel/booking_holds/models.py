from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now, timedelta
from pawtel.customers.models import Customer
from pawtel.room_types.models import RoomType


def default_hold_expiry():
    return now() + timedelta(minutes=10)


class BookingHold(models.Model):

    # Attributes -------------------------------------------------------------

    hold_expires_at = models.DateTimeField(default=default_hold_expiry, null=False)

    # Transient attributes ---------------------------------------------------

    def is_expired(self):
        return now() > self.hold_expires_at

    # Relations --------------------------------------------------------------

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"Booking hold of room_type.name by {self.customer.username}"

    def clean(self):
        if self.hold_expires_at and self.hold_expires_at < now():
            raise ValidationError(
                {"hold_expires_at": "Hold expiration date cannot be in the past."}
            )
