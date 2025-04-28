from datetime import date

from django.core.validators import MinValueValidator
from django.db import models
from django.forms import ValidationError
from pawtel.customers.models import Customer
from pawtel.room_types.models import RoomType


class Booking(models.Model):
    creation_date = models.DateField(null=False, auto_now_add=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        null=False,
        blank=False,
    )

    # Relations --------------------------------------------------------------

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=False)

    # Meta configuration -----------------------------------------------------

    def __str__(self):
        return f"Booking {self.id}: {self.start_date} - {self.end_date}"

    def clean(self):
        super().clean()

        today = date.today()
        errors = {}

        if not self.creation_date:
            self.creation_date = today

        if self.creation_date > today:
            errors.setdefault("creation_date", []).append(
                "La fecha de comienzo de la reserva debe ser futura."
            )

        if self.start_date and self.start_date <= today:
            errors.setdefault("start_date", []).append(
                "La fecha de comienzo de la reserva debe ser futura."
            )

        if self.end_date and self.end_date <= today:
            errors.setdefault("end_date", []).append(
                "La fecha de finalización de la reserva debe ser futura."
            )

        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                errors.setdefault("end_date", []).append(
                    "La fecha de finalización de la reserva no puede ser anterior a la fecha de comienzo de la reserva."
                )

            if (self.end_date - self.start_date).days >= 186:
                errors.setdefault("end_date", []).append(
                    "La duración de la reserva no puede exceder 6 meses (186 días)."
                )

        if errors:
            raise ValidationError(errors)
