from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from pawtel.bookings.models import Booking
from pawtel.room_types.models import RoomType

THREE_YEARS = timedelta(days=3 * 365)


@shared_task
def delete_archived_room_types_without_recent_bookings():
    today = timezone.now().date()
    threshold_date = today - THREE_YEARS

    total_deleted = 0
    archived_roomtypes = RoomType.objects.filter(is_archived=True)
    for rt in archived_roomtypes:
        if not Booking.objects.filter(
            room_type=rt, start_date__gte=threshold_date
        ).exists():
            count, _ = rt.delete()
            total_deleted += count

    return f"Cleanup de RoomTypes archivados completado. Eliminados: {total_deleted}"
