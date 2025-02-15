from django.urls import path
from .views import random_pets

urlpatterns = [
    path('random-pets/', random_pets, name='random-pets'),
]