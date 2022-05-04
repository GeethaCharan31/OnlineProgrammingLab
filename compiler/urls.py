from django.urls import path
from . import views  # importing  views of the app-base

urlpatterns = [
    path('room/<str:pk>/<str:pk2>', views.question, name="question"),
]
