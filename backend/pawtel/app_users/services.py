from pawtel.app_users.models import AppUser, UserRole
from pawtel.app_users.serializers import AppUserSerializer
from rest_framework.exceptions import (AuthenticationFailed, NotFound,
                                       ValidationError)


class AppUserService:

    # General processes ------------------------------------------------------

    @staticmethod
    def general_create_app_user(request):
        """This will be called from the views of AuthApp, through the service of each role."""
        input_serializer = AppUserService.__serialize_input_app_user_create(request)
        AppUserService.__validate_create_app_user(input_serializer)
        app_user_created = AppUserService.__create_app_user(input_serializer)
        return app_user_created

    @staticmethod
    def general_update_app_user(request, pk):
        """This will be called from the views of each role."""
        AppUserService.__authorize_action_app_user(request, pk)
        input_serializer = AppUserService.__serialize_input_app_user_update(request, pk)
        AppUserService.__validate_update_app_user(pk, input_serializer)
        AppUserService.__update_app_user(pk, input_serializer)

    @staticmethod
    def general_delete_app_user(request, pk):
        """This will be called from the views of each role."""
        AppUserService.__authorize_action_app_user(request, pk)
        AppUserService.__delete_app_user(pk)

    # Common -----------------------------------------------------------------

    @staticmethod
    def __authorize_action_app_user(request, pk):
        AppUserService.retrieve_app_user(pk)

    @staticmethod
    def get_current_app_user(request):
        if (not request.user) or (not request.user.is_authenticated):
            raise AuthenticationFailed("User is not authenticated.")

        app_user = AppUserService.retrieve_app_user(request.user.id)
        return app_user

    @staticmethod
    def get_current_role_user(request):
        app_user = AppUserService.get_current_app_user(request)

        if app_user.role == UserRole.CUSTOMER:
            return app_user.customer
        if app_user.role == UserRole.HOTEL_OWNER:
            return app_user.hotel_owner

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_app_user(pk, allow_inactive=False):
        try:
            if allow_inactive:
                return AppUser.objects.get(id=pk)
            else:
                return AppUser.objects.get(id=pk, is_active=True)
        except AppUser.DoesNotExist:
            raise NotFound(detail="User not found.")

    # POST -------------------------------------------------------------------

    @staticmethod
    def __serialize_input_app_user_create(request):
        context = {"request": request}
        serializer = AppUserSerializer(data=request.data, context=context)
        return serializer

    @staticmethod
    def __validate_create_app_user(input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        email = input_serializer.validated_data.get("email")
        phone = input_serializer.validated_data.get("phone")

        if AppUser.objects.filter(email=email).exists():
            raise ValidationError({"email": "Email already in use."})

        if AppUser.objects.filter(phone=phone).exists():
            raise ValidationError({"phone": "Phone number already in use."})

    @staticmethod
    def __create_app_user(input_serializer):
        app_user = input_serializer.save()
        return app_user

    # PUT/PATCH --------------------------------------------------------------

    @staticmethod
    def __serialize_input_app_user_update(request, pk):
        app_user = AppUserService.retrieve_app_user(pk)
        context = {"request": request}
        serializer = AppUserSerializer(
            instance=app_user, data=request.data, context=context
        )
        return serializer

    @staticmethod
    def __validate_update_app_user(pk, input_serializer):
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)

        username = input_serializer.validated_data.get("username")
        email = input_serializer.validated_data.get("email")
        phone = input_serializer.validated_data.get("phone")

        if (
            username
            and AppUser.objects.filter(username=username).exclude(id=pk).exists()
        ):
            raise ValidationError({"username": "Username in use."})

        if email and AppUser.objects.filter(email=email).exclude(id=pk).exists():
            raise ValidationError({"email": "Email in use."})

        if phone and AppUser.objects.filter(phone=phone).exclude(id=pk).exists():
            raise ValidationError({"phone": "Phone in use."})

    @staticmethod
    def __update_app_user(pk, input_serializer):
        app_user = AppUserService.retrieve_app_user(pk)
        return input_serializer.update(app_user, input_serializer.validated_data)

    # DELETE -----------------------------------------------------------------

    @staticmethod
    def __delete_app_user(pk):
        app_user = AppUserService.retrieve_app_user(pk)
        app_user.delete()
