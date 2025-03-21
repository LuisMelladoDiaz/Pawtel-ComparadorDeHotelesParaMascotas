from authapp.views import LoginView, RegisterView, UserInfoView
from django.urls import path

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("user-info/", UserInfoView.as_view(), name="view user info"),
    path("register/", RegisterView.as_view(), name="register"),
]
