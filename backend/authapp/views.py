from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        # Crear el refresh token y el access token
        refresh = RefreshToken.for_user(user)
        response_data = {
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        response = Response(response_data)

        # Establecer las cookies con el JWT
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],  # 'access_token'
            value=str(refresh.access_token),
            httponly=True,
            samesite="None",  # o 'Strict', según lo que necesites
            secure=True,  # Asegúrate de tener HTTPS
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            samesite="None",
            secure=True,  # Asegúrate de tener HTTPS
        )

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Eliminar las cookies con los tokens JWT
        response = Response({"message": "Logged out successfully"})
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie("refresh_token")
        return response


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]  # Asegura que el usuario esté autenticado

    def get(self, request):
        user = request.user  # El usuario está disponible después de la autenticación
        return Response(
            {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
