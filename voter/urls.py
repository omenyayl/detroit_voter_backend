from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('votes/<slug:room_id>', delete_room),
]
