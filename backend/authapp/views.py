from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        # Crear el token de refresh
        refresh = RefreshToken.for_user(user)

        # Respuesta con los tokens
        response_data = {
            "message": "Login successful",
            "access": str(refresh.access_token),  # Incluye el access_token
            "refresh": str(refresh),  # Incluye el refresh_token
        }

        # Establecer cookies para los tokens (si es necesario)
        response = Response(response_data)
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=str(refresh.access_token),
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            samesite="Lax",
            secure=False,
        )

        return response



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Aseguramos que el usuario está autenticado

    def post(self, request):
        # Eliminar las cookies de los tokens
        response = Response({"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        # Si quieres agregar más limpieza en sesión o alguna otra acción, también puedes hacerlo aquí
        return response


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })