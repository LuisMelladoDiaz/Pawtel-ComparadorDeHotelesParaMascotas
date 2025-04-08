from celery import shared_task
from django.utils import timezone
from pawtel.booking_holds.models import BookingHold


@shared_task
def delete_inactive_bookingholds():
    count, _ = BookingHold.objects.filter(hold_expires_at__lt=timezone.now()).delete()
    return f"Eliminados {count} booking_holds inactivos."
