from django.urls import path
from . import views  # importing  views of the app-base

urlpatterns = [
    path('home/', views.home, name="home"),  # urls
    path('room/<str:pk>/', views.room, name="room"),
    path('room/<str:pk>/<str:pk2>', views.question, name="question"),

    path('create_room/', views.createRoom, name="createRoom"),
    path('update_room/<str:pk>', views.updateRoom, name="updateRoom"),
    path('delete_room/<str:pk>', views.deleteRoom, name="deleteRoom"),
]
