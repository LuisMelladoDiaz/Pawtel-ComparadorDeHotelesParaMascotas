from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from pawtel.customers.models import Customer
from pawtel.room_types.models import RoomType


class BookingHold(models.Model):

    # Attributes -------------------------------------------------------------

    hold_expires_at = models.DateTimeField(null=False, blank=False)

    booking_start_date = models.DateField(null=False, blank=False)

    booking_end_date = models.DateField(null=False, blank=False)

    # Transient attributes ---------------------------------------------------

    @property  # use this withouth ()
    def is_expired(self):
        return now() > self.hold_expires_at

    # Relations --------------------------------------------------------------

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"Booking hold of {self.room_type.name} by {self.customer.username}"

    def clean(self):
        super().clean()

        if (self.hold_expires_at) and (self.hold_expires_at) < now():
            raise ValidationError(
                {"hold_expires_at": "Hold expiration date cannot be in the past."}
            )

        if (self.booking_start_date) and (self.booking_start_date) <= date.today():
            raise ValidationError(
                {"booking_start_date": "Booking start date must be in the future."}
            )

        if (self.booking_end_date) and (self.booking_end_date) <= date.today():
            raise ValidationError(
                {"booking_end_date": "Booking end date must be in the future."}
            )

        if (
            (self.booking_start_date)
            and (self.booking_end_date)
            and (self.booking_end_date < self.booking_start_date)
        ):
            raise ValidationError(
                {
                    "booking_end_date": "Booking end date cannot be earlier than booking start date."
                }
            )
