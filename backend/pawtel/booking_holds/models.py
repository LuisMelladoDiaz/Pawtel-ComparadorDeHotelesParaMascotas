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
        return (
            f"Booking hold of {self.room_type.name} by {self.customer.user.username}"
            f" from {self.booking_start_date} to {self.booking_end_date}"
        )

    def clean(self):
        super().clean()

        errors = {}

        if self.hold_expires_at and self.hold_expires_at < now():
            errors.setdefault("hold_expires_at", []).append(
                "La fecha de expiración de la Booking Hold no puede ser pasada."
            )

        if self.booking_start_date and self.booking_start_date <= date.today():
            errors.setdefault("booking_start_date", []).append(
                "La fecha de comienzo de la reserva debe ser futura."
            )

        if self.booking_end_date and self.booking_end_date <= date.today():
            errors.setdefault("booking_end_date", []).append(
                "La fecha de finalización de la reserva debe ser futura."
            )

        if self.booking_start_date and self.booking_end_date:
            if self.booking_end_date < self.booking_start_date:
                errors.setdefault("booking_end_date", []).append(
                    "La fecha de finalización de la reserva no puede ser anterior a la fecha de comienzo de la reserva."
                )

            if (self.booking_end_date - self.booking_start_date).days >= 186:
                errors.setdefault("booking_end_date", []).append(
                    "La duración de la reserva no puede exceder 6 meses (186 días)."
                )

        if errors:
            raise ValidationError(errors)
