from django.urls import path
from . import views  # importing  views of the app-base

urlpatterns = [
    path('', views.home, name="home"),  # urls
    path('second/', views.second, name="second"),
]
