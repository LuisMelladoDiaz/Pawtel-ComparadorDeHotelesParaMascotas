from django.db import models
from django.utils.timezone import now, timedelta
from pawtel.customers.models import Customer
from pawtel.room_types.models import RoomType


class BookingHold(models.Model):

    # Attributes -------------------------------------------------------------

    hold_expires_at = models.DateTimeField(
        default=lambda: now() + timedelta(minutes=10), null=False
    )

    # Transient attributes ---------------------------------------------------

    def is_expired(self):
        return now() > self.hold_expires_at

    # Relations --------------------------------------------------------------

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"Booking hold of room_type.name by {self.customer.username}"
