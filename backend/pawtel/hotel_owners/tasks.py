from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from pawtel.bookings.models import Booking
from pawtel.hotel_owners.models import HotelOwner

THREE_YEARS = timedelta(days=3 * 365)


@shared_task
def delete_inactive_hotel_owners_without_recent_bookings():
    today = timezone.now().date()
    threshold_date = today - THREE_YEARS
    total_deleted = 0

    hotel_owners = HotelOwner.objects.select_related("user").all()
    for owner in hotel_owners:
        if not owner.user.is_active:
            if not Booking.objects.filter(
                room_type__hotel__hotel_owner=owner, start_date__gte=threshold_date
            ).exists():
                owner.user.delete()
                total_deleted += 1

    return f"Eliminados {total_deleted} hotel owners inactivos."
