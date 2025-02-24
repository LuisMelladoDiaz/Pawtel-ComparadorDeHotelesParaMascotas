from django.urls import path
from authapp.views import LoginView, LogoutView, UserInfoView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user-info/", UserInfoView.as_view(), name="view user info"),
]
