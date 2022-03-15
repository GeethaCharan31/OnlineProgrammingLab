from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Question
from .forms import RoomForm, QuestionForm, SolutionForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''  # for searching
    # rooms = Room.objects.filter(name__icontains=q)
    rooms = Room.objects.filter(
        Q(name__icontains=q)  # |
        # Q(description__icontains=q) #add search by user too
    )

    room_count = rooms.count()

    context = {'rooms': rooms, 'room_count': room_count}
    return render(request, "home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    questions = Question.objects.filter(room=pk)
    context = {'room': room, 'questions': questions}

    return render(request, "room.html", context)


def question(request, pk, pk2):
    """
    For Submission
    """
    form = SolutionForm()
    # above one for form
    question = Question.objects.get(id=pk2)
    context = {'question': question, 'form': form}
    return render(request, "question.html", context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createQuestion')

    context = {'form': form}
    return render(request, "form.html", context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # checking for valid host
    if request.user != room.host:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save();
            return redirect('home')

    context = {'form': form}
    return render(request, "form.html", context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # checking for valid host
    if request.user != room.host:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, "delete.html", {'obj': room})


@login_required(login_url='login')
def createQuestion(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createQuestion')

    context = {'form': form}
    return render(request, "question_form.html", context)


def finalSubmit(request):
    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
    context = {}
    return render(request, "submitted.html", context)
