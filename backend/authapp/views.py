from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from pawtel.app_users.models import AppUser
from pawtel.app_users.serializers import AppUserSerializer
from pawtel.customers.services import CustomerService
from pawtel.hotel_owners.services import HotelOwnerService
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"error": "Credenciales incorrectas"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        response_data = {
            "detail": "Inicio de sesión exitoso",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer_data = AppUserSerializer(user).data

        if hasattr(user, "hotel_owner"):
            hotel_owner_id = user.hotel_owner.id
            user_serializer_data["hotel_owner_id"] = hotel_owner_id
            user_serializer_data["role"] = "hotel_owner"

        elif hasattr(user, "customer"):
            customer_id = user.customer.id
            user_serializer_data["customer_id"] = customer_id
            user_serializer_data["role"] = "customer"

        elif hasattr(user, "admin"):
            user_serializer_data["role"] = "admin"
            user_serializer_data["admin_id"] = user.admin.id

        return Response(user_serializer_data)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get("role")
        object = None

        if role == "hotel_owner":
            object = HotelOwnerService.general_create_hotel_owner(request)
        elif role == "customer":
            object = CustomerService.general_create_customer(request)

        else:
            return Response(
                {"error": "Rol inválido. Sólo se permiten dueños de hotel y clientes"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(object, status=status.HTTP_201_CREATED)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "El email es necesario"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = AppUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            frontend_url = (
                f"{settings.FRONTEND_URL}/auth/password-reset-confirm/{uidb64}/{token}/"
            )
            message = (
                f"Ha solicitado restablecer la contraseña. Para continuar el proceso haga click en el siguiente enlace:\n\n"
                f"{frontend_url}\n\n"
                "Si no has solicitado cambiar la contraseña, por favor contáctanos de inmediato a nuestro email: "
                f"{settings.DEFAULT_FROM_EMAIL}"
            )
            send_mail(
                "Restablezca su contraseña",
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response(
                {"message": "Email para restablecer contraseña enviado"},
                status=status.HTTP_200_OK,
            )
        except AppUser.DoesNotExist:
            return Response(
                {"error": "No existe un usuario con este email"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = AppUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            password = request.data.get("password")
            if password:
                if user.check_password(password):
                    return Response(
                        {
                            "error": "La nueva contraseña no puede ser la misma que la anterior."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(password)
                user.save()
                return Response(
                    {"message": "La contraseña se ha cambiado correctamente."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Se necesita una contraseña."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Id inválido."}, status=status.HTTP_400_BAD_REQUEST
            )
