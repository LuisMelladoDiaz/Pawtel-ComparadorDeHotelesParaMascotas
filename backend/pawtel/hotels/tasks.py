from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from pawtel.hotels.models import Hotel

THREE_YEARS = timedelta(days=3 * 365)


@shared_task
def delete_archived_hotels_without_recent_bookings():
    today = timezone.now().date()
    threshold_date = today - THREE_YEARS

    total_deleted = 0
    archived_hotels = Hotel.objects.filter(is_archived=True)
    for hotel in archived_hotels:
        roomtypes = hotel.roomtype_set.all()
        has_recent_booking = any(
            Booking.objects.filter(
                room_type=rt, start_date__gte=threshold_date
            ).exists()
            for rt in roomtypes
        )
        if not has_recent_booking:
            count, _ = hotel.delete()
            total_deleted += count

    return f"Cleanup de Hotels archivados completado. Eliminados: {total_deleted}"
