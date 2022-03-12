from django.shortcuts import render, redirect
from .models import Room, Question
from .forms import RoomForm


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


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, "form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save();
            return redirect('home')

    context = {'form': form}
    return render(request, "form.html", context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, "delete.html", {'obj':room})