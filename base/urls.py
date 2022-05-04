from django.urls import path
from . import views  # importing  views of the app-base

urlpatterns = [
    path('home/', views.home, name="home"),  # urls
    path('room/<str:pk>/', views.room, name="room"),
    # path('room/<str:pk>/<str:pk2>', views.question, name="question"), - this is view_question, shifted to compiler app

    path('create_room/', views.createRoom, name="createRoom"),

    path('update_room/<str:pk>', views.updateRoom, name="updateRoom"),
    path('delete_room/<str:pk>', views.deleteRoom, name="deleteRoom"),

    # view responses
    path('room_responses/<str:pk>', views.roomResponses, name="roomResponses"),
    path('question_responses/<str:pk>/<str:pk2>', views.questionResponses, name="questionResponses"),

    # path('view_response/<str:pk>/<str:pk2>/<str:pk3>/', views.viewResponses, name="viewResponses"),
    path('delete_response/<str:pk>/<str:pk2>/<str:pk3>/', views.deleteResponse, name="deleteResponse"),

    path('create_question/<str:pk>', views.createQuestion, name="createQuestion"),
    # path('create_question2/', views.createQuestion2, name="createQuestion2"),
    path('update_question/<str:pk>/<str:pk2>', views.updateQuestion, name="updateQuestion"),
    path('delete_question/<str:pk>/<str:pk2>', views.deleteQuestion, name="deleteQuestion"),

    # path('final_submit/', views.finalSubmit, name="finalSubmit"),
]
