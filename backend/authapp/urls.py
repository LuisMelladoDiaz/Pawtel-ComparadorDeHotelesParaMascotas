from authapp.views import (LoginView, PasswordResetConfirmView,
                           PasswordResetView, RegisterView, UserInfoView)
from django.urls import path

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("user-info/", UserInfoView.as_view(), name="view user info"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "email-password-reset/", PasswordResetView.as_view(), name="email new password"
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password reset",
    ),
]
