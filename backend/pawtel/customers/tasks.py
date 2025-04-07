from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from pawtel.bookings.models import Booking
from pawtel.customers.models import Customer

THREE_YEARS = timedelta(days=3 * 365)


@shared_task
def delete_inactive_customers_without_recent_bookings():
    today = timezone.now().date()
    threshold_date = today - THREE_YEARS
    total_deleted = 0

    customers = Customer.objects.select_related("user").all()
    for customer in customers:
        if not customer.user.is_active:
            if not Booking.objects.filter(
                customer=customer, creation_date__gte=threshold_date
            ).exists():
                customer.user.delete()
                total_deleted += 1

    return f"Eliminados {total_deleted} customers inactivos."
