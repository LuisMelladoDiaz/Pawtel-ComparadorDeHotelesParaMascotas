from pawtel.app_users.models import AppUser
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
        """This will be called from the views of of each role."""
        AppUserService.__authorize_action_app_user(request, pk)
        input_serializer = AppUserService.__serialize_input_app_user_update(request, pk)
        AppUserService.__validate_update_app_user(pk, input_serializer)
        AppUserService.__update_app_user(pk, input_serializer)

    @staticmethod
    def general_delete_app_user(request, pk):
        """This will be called from the views of of each role."""
        AppUserService.__authorize_action_app_user(request, pk)
        AppUserService.__delete_app_user(pk)

    # Common -----------------------------------------------------------------

    @staticmethod
    def __authorize_action_app_user(request, pk):
        app_user = AppUserService.retrieve_app_user(pk)

        if (not app_user) or (not app_user.is_active):
            raise NotFound("App user does not exist.")

    # GET --------------------------------------------------------------------

    @staticmethod
    def retrieve_app_user(pk, allow_inactive=False):
        try:
            return AppUser.objects.get(id=pk)
        except AppUser.DoesNotExist:
            raise NotFound(detail=f"User not found.")

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

    # OTHERS -----------------------------------------------------------------

    @staticmethod
    def get_current_app_user(request):
        if (not request.user) or (not request.user.is_authenticated):
            raise AuthenticationFailed("User is not authenticated.")

        app_user = AppUser.objects.get(user_id=request.user.id)
        if (not app_user) or (not app_user.is_active):
            raise NotFound("User does not exist.")

        return app_user
