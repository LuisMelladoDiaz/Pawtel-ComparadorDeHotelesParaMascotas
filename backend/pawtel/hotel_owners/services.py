from datetime import date, timedelta

from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.bookings.models import Booking
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotels.models import Hotel
from pawtel.permission_services import PermissionService
from pawtel.room_types.models import RoomType
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)


class HotelOwnerService:

    THREE_YEARS = timedelta(days=3 * 365)

    # General processes ------------------------------------------------------

    @staticmethod
    def general_create_hotel_owner(request):
        """This will be called from the views of AuthApp."""
        app_user = AppUserService.general_create_app_user(request)
        hotel_owner_created = HotelOwnerService.__create_hotel_owner(app_user.id)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(
            hotel_owner_created
        )
        return output_serializer_data

    # Authorize --------------------------------------------------------------

    def authorize_action_hotel_owner(
        request, action_name, target_hotel_owner_id=None, check_ownership=False
    ):
        role_user = AppUserService.get_current_role_user(request)
        HotelOwnerService.check_approval_hotel_owner(role_user)
        PermissionService.check_permission_hotel_owner_service(role_user, action_name)

        if target_hotel_owner_id:
            target_hotel_owner = HotelOwnerService.__perform_retrieve_hotel_owner(
                role_user, target_hotel_owner_id
            )
            if check_ownership:
                HotelOwnerService.__check_ownership_hotel_owner(
                    role_user, target_hotel_owner
                )

        return role_user

    def __perform_retrieve_hotel_owner(role_user, target_hotel_owner_id):
        if role_user.user.role == UserRole.ADMIN:
            return HotelOwnerService.retrieve_hotel_owner(target_hotel_owner_id, True)
        else:
            return HotelOwnerService.retrieve_hotel_owner(target_hotel_owner_id)

    def __check_ownership_hotel_owner(role_user, target_hotel_owner):
        if role_user.user.role == UserRole.ADMIN:
            return
        elif role_user.user.role == UserRole.HOTEL_OWNER:
            if target_hotel_owner.id != role_user.id:
                raise PermissionDenied("Permiso denegado.")
        else:
            raise PermissionDenied("Permiso denegado.")

    def check_approval_hotel_owner(role_user):
        if role_user.user.role == UserRole.HOTEL_OWNER:
            if not role_user.is_approved:
                raise PermissionDenied("El dueño de hotel no está aprobado.")
        return

    # Serialization -----------------------------------------------------------------

    @staticmethod
    def serialize_output_hotel_owner(hotel_owner, many=False):
        return HotelOwnerSerializer(hotel_owner, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel_owner(pk, allow_inactive=False):
        try:
            if allow_inactive:
                return HotelOwner.objects.get(id=pk)
            else:
                return HotelOwner.objects.get(id=pk, user__is_active=True)
        except HotelOwner.DoesNotExist:
            raise NotFound(detail="Dueño de hotel no encontrado.")

    @staticmethod
    def get_hotel_owner_by_user(app_user_id):
        try:
            return HotelOwner.objects.get(user_id=app_user_id)
        except HotelOwner.DoesNotExist:
            raise NotFound("El dueño de hotel no existe.")

    @staticmethod
    def get_current_hotel_owner(request):
        app_user = AppUserService.get_current_app_user(request)
        hotel_owner = HotelOwnerService.get_hotel_owner_by_user(app_user)
        return hotel_owner

    @staticmethod
    def list_hotel_owners(allow_inactive=False):
        if allow_inactive:
            return HotelOwner.objects.all()
        else:
            return HotelOwner.objects.filter(user__is_active=True)

    @staticmethod
    def list_unapproved_hotel_owners():
        return HotelOwner.objects.filter(is_approved=False)

    # POST -------------------------------------------------------------------

    @staticmethod
    def __create_hotel_owner(app_user_id):
        return HotelOwner.objects.create(user_id=app_user_id)

    # Delete -----------------------------------------------------------------

    @staticmethod
    def validate_all_hotels_deletion(hotel_owner_pk):
        hotel_owner = HotelOwner.objects.get(pk=hotel_owner_pk)
        hotels = Hotel.objects.filter(hotel_owner=hotel_owner)
        today = date.today()
        delete = True

        for hotel in hotels:
            room_types = RoomType.objects.filter(hotel=hotel)
            for room_type in room_types:
                past_limit = today - HotelOwnerService.THREE_YEARS
                recent_bookings = Booking.objects.filter(
                    room_type_id=room_type.id, start_date__range=(past_limit, today)
                )
                future_bookings = Booking.objects.filter(
                    room_type_id=room_type.id, start_date__gte=today
                )

                if future_bookings.exists():
                    raise ValidationError(
                        {
                            "detail": "El objeto no se puede eliminar porque existe una reserva asociada próximamente."
                        }
                    )

                if recent_bookings.exists():
                    delete = False
                    break

        return delete

    # Hotels -----------------------------------------------------------------

    @staticmethod
    def list_hotels_of_hotel_owner(hotel_owner_id):
        return Hotel.objects.filter(hotel_owner_id=hotel_owner_id, is_archived=False)

    @staticmethod
    def delete_all_hotels_of_hotel_owner(hotel_owner_id):
        hotels_to_delete = Hotel.objects.filter(
            hotel_owner_id=hotel_owner_id, is_archived=False
        )
        if not hotels_to_delete.exists():
            raise PermissionDenied("No existen hoteles para borrar.")

        hotels_to_delete.delete()

    @staticmethod
    def approve_hotel_owner_patch(hotel_owner_id):
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(hotel_owner_id)
        hotel_owner.is_approved = True
        hotel_owner.save()
        return hotel_owner

    @staticmethod
    def delete_unapproved_hotel_owner(hotel_owner_id):
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(hotel_owner_id)

        if hotel_owner.is_approved:
            raise PermissionDenied(
                "Solo se pueden eliminar dueños de hotel no aprobados."
            )

        hotel_owner.user.delete()
