from django.contrib.auth import authenticate
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
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        response_data = {
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer_data = AppUserSerializer(user).data
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
                {"error": "Invalid role. Only hotel owners and customers are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(object, status=status.HTTP_201_CREATED)
