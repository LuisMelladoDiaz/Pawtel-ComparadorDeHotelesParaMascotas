from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from pawtel.bookings.models import Booking

THREE_YEARS = timedelta(days=3 * 365)


@shared_task
def delete_old_bookings():
    today = timezone.now().date()
    threshold_date = today - THREE_YEARS

    count, _ = Booking.objects.filter(creation_date__lt=threshold_date).delete()

    return f"Eliminadas {count} bookings con creation_date anterior a 3 años."
