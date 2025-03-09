from django.forms import ValidationError
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import NotFound, PermissionDenied


class HotelOwnerService:

    # Common -----------------------------------------------------------------

    @staticmethod
    def authorize_action_hotel_owner(request, pk):
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)

        if not hotel_owner:
            raise NotFound("Hotel owner does not exist.")

        if not hotel_owner.is_active:
            raise PermissionDenied("")

    @staticmethod
    def serialize_output_hotel_owner(hotel_owner, many=False):
        return HotelOwnerSerializer(hotel_owner, many=many).data

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_hotel_owner(pk):
        return HotelOwner.objects.get(id=pk)

    # POST -------------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_owner_create(request):
        context = {"request": request}
        serializer = HotelOwnerSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def validate_create_hotel_owner(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        email = input_serializer.validated_data.get("email")
        phone = input_serializer.validated_data.get("phone")

        if HotelOwner.objects.filter(email=email).exists():
            raise ValidationError({"email": "Email already in use."})

        if HotelOwner.objects.filter(phone=phone).exists():
            raise ValidationError({"phone": "Phone number already in use."})

    @staticmethod
    def create_hotel_owner(input_serializer):
        hotel_owner = input_serializer.save()
        return hotel_owner

    # PUT/PATCH --------------------------------------------------------------

    @staticmethod
    def serialize_input_hotel_owner_update(request, pk):
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
        context = {"request": request}
        serializer = HotelOwnerSerializer(
            instance=hotel_owner, data=request.data, context=context
        )
        return serializer

    @staticmethod
    def validate_update_hotel_owner(pk, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        username = input_serializer.validated_data.get("username")
        email = input_serializer.validated_data.get("email")
        phone = input_serializer.validated_data.get("phone")

        if (
            username
            and HotelOwner.objects.filter(username=username).exclude(id=pk).exists()
        ):
            raise ValidationError({"username": "Username in use."})

        if email and HotelOwner.objects.filter(email=email).exclude(id=pk).exists():
            raise ValidationError({"email": "Email in use."})

        if phone and HotelOwner.objects.filter(phone=phone).exclude(id=pk).exists():
            raise ValidationError({"phone": "Phone in use."})

    @staticmethod
    def update_hotel_owner(pk, input_serializer):
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
        return input_serializer.update(hotel_owner, input_serializer.validated_data)

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def delete_hotel_owner(pk):
        hotel_owner = HotelOwnerService.retrieve_hotel_owner(pk)
        hotel_owner.delete()

    # OTHERS -----------------------------------------------------------------

    @staticmethod
    def get_all_hotels_of_hotel_owner(hotel_owner_id):
        return Hotel.objects.filter(hotel_owner_id=hotel_owner_id, is_archived=False)

    @staticmethod
    def delete_all_hotels_of_hotel_owner(hotel_owner_id):
        hotels_to_delete = Hotel.objects.filter(
            hotel_owner_id=hotel_owner_id, is_archived=False
        )
        if not hotels_to_delete.exists():
            raise PermissionDenied("No hotels to delete.")

        hotels_to_delete.delete()
