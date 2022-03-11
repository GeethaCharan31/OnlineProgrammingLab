from django.shortcuts import render
from .models import Room, Question


# Create your views here.

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, "home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    questions = Question.objects.filter(room=pk)
    context = {'room': room, 'questions': questions}

    return render(request, "room.html", context)


def question(request, pk, pk2):
    question = Question.objects.get(id=pk2)
    context = {'question': question}
    return render(request, "question.html", context)


def form(request):
    return render(request, "form.html")
