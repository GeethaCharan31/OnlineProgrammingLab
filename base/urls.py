from django.urls import path
from . import views  # importing  views of the app-base

urlpatterns = [
    path('home/', views.home, name="home"),  # urls
    path('form/', views.form, name="form"),
    path('room/<str:pk>/', views.room, name="room"),
    path('room/<str:pk>/<str:pk2>', views.question, name="question"),
]
