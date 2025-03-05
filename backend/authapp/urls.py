from authapp.views import LoginView, LogoutView, UserInfoView
from django.urls import path

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user-info/", UserInfoView.as_view(), name="view user info"),
]
