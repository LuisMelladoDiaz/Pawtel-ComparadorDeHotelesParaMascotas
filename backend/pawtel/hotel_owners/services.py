from django.forms import ValidationError
from pawtel.hotel_owners.models import HotelOwner
from pawtel.hotel_owners.serializers import HotelOwnerSerializer
from pawtel.hotels.models import Hotel
from rest_framework.exceptions import NotFound, PermissionDenied


class HotelOwnerService:

    @staticmethod
    def authorize_action_hotel_owner(request, pk):

        hotel_owner = HotelOwner.objects.get(id=pk)

        if not hotel_owner:
            raise NotFound("Hotel owner does not exist.")

        if not hotel_owner.is_active:
            raise PermissionDenied("")

    @staticmethod
    def retrieve_hotel_owner(request, pk):
        return HotelOwner.objects.get(id=pk)

    @staticmethod
    def serialize_input_hotel_owner_create(request):
        serializer = HotelOwnerSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_create_hotel_owner(serializer, user):
        email = serializer.validated_data.get("email")
        phone = serializer.validated_data.get("phone")

        if HotelOwner.objects.filter(email=email).exists():
            raise ValidationError({"email": "Email already in use."})

        if HotelOwner.objects.filter(phone=phone).exists():
            raise ValidationError({"phone": "Phone number already in use."})

    @staticmethod
    def create_hotel_owner(serializer):
        hotel_owner = serializer.save()
        return hotel_owner

    @staticmethod
    def serialize_input_hotel_owner_update(request, pk):
        data = {
            key: value
            for key, value in request.data.items()
            if key
            in HotelOwnerSerializer.fields_required_for_post
            + HotelOwnerSerializer.fields_editable
        }
        serializer = HotelOwnerSerializer(data=data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def validate_semantically_update_hotel_owner(pk, input_serializer):
        input_serializer.is_valid(raise_exception=True)

        hotel_owner = HotelOwner.objects.get(id=pk)

        email = input_serializer.validated_data.get("email")
        if email and email != hotel_owner.email:
            if HotelOwner.objects.filter(email=email).exists():
                raise ValidationError({"email": "Email in use"})

        phone = input_serializer.validated_data.get("phone")
        if phone and phone != hotel_owner.phone:
            if HotelOwner.objects.filter(phone=phone).exists():
                raise ValidationError({"phone": "Phone in use."})

        return True

    @staticmethod
    def update_hotel_owner(pk, input_serializer):
        hotel_owner = HotelOwner.objects.get(id=pk)
        return input_serializer.update(hotel_owner, input_serializer.validated_data)

    @staticmethod
    def serialize_output_hotel_owner(hotel_owner):
        return HotelOwnerSerializer(hotel_owner).data

    @staticmethod
    def validate_semantically_partial_update_hotel_owner(pk, input_serializer):
        input_serializer.is_valid(raise_exception=True)

        hotel_owner = HotelOwner.objects.get(id=pk)

        email = input_serializer.validated_data.get("email")
        if email and email != hotel_owner.email:
            if HotelOwner.objects.filter(email=email).exists():
                raise ValidationError({"email": "Email in use"})

        phone = input_serializer.validated_data.get("phone")
        if phone and phone != hotel_owner.phone:
            if HotelOwner.objects.filter(phone=phone).exists():
                raise ValidationError({"phone": "Phone in use."})

        return True

    @staticmethod
    def serialize_input_hotel_owner_partial_update(request, pk):
        data = {
            key: value
            for key, value in request.data.items()
            if key
            in HotelOwnerSerializer.fields_required_for_post
            + HotelOwnerSerializer.fields_editable
        }
        serializer = HotelOwnerSerializer(data=data, partial=True)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer

    @staticmethod
    def partial_update_hotel_owner(pk, input_serializer):
        hotel_owner = HotelOwner.objects.get(id=pk)
        return input_serializer.update(hotel_owner, input_serializer.validated_data)

    @staticmethod
    def delete_hotel_owner(pk):
        hotel_owner = HotelOwner.objects.get(id=pk)
        hotel_owner.delete()

    @staticmethod
    def get_all_hotels_of_hotel_owner(hotel_owner_id):

        return Hotel.objects.filter(hotel_owner_id=hotel_owner_id, is_archived=False)

    @staticmethod
    def delete_all_hotels_of_hotel_owner(hotel_owner_id):

        hotels = Hotel.objects.filter(hotel_owner_id=hotel_owner_id, is_archived=False)
        if not hotels.exists():
            raise PermissionDenied("No hotels to delete.")

        hotels.delete()
