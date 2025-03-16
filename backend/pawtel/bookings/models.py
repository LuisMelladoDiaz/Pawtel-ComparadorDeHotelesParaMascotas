from django.db import models
from django.core.validators import MinValueValidator
from datetime import date

class Booking(models.Model):
    creation_date = models.DateField(null=False, auto_now_add=True) 
    start_date = models.DateField(null=False, blank=False) 
    end_date = models.DateField(null=False, blank=False)  
    total_price = models.DecimalField( decimal_places=2, validators=[MinValueValidator(1.00)], null=False, blank=False)
    

    # Relations --------------------------------------------------------------

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)



    def clean(self):
        """✅ Validaciones personalizadas para comprobar restricciones sintácticas de las fechas"""
        super().clean()

        if self.creation_date > date.today():
            raise ValidationError({"creation_date": "La fecha de creación no puede estar en el futuro"})

        if self.start_date <= date.today():
            raise ValidationError({"start_date": "La fecha de inicio debe ser en el futuro"})
    
        if self.end_date <= date.today():
            raise ValidationError({"end_date": "La fecha de fin debe ser en el futuro"})



    def __str__(self):
        return f"Booking {self.id}: {self.start_date} - {self.end_date})"