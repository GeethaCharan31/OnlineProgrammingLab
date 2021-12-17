from django.urls import path
from . import views  # importing  views of the app-authentication

urlpatterns = [
    path('', views.login, name="login"),  # urls
    path('signup/', views.signup, name="signup"),
]
