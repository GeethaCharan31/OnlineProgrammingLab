from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Question, Solution
from .forms import RoomForm, QuestionForm, SolutionForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''  # for searching
    # rooms = Room.objects.filter(name__icontains=q)
    rooms = Room.objects.filter(
        Q(name__icontains=q), verified=True
        # Q(description__icontains=q) #add search by user too
    )

    room_count = rooms.count()

    context = {'rooms': rooms, 'room_count': room_count}
    return render(request, "home.html", context)

@login_required(login_url='login')
def myRooms(request):
    resultset=Room.objects.filter(host=request.user)

    myroomsFlag=True
    room_count = resultset.count()
    context = {'rooms':resultset,'room_count': room_count,'myroomsFlag':myroomsFlag}
    return render(request, "home.html", context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    questions = Question.objects.filter(room=pk)
    context = {'room': room, 'questions': questions}

    return render(request, "room.html", context)



# remove this view as it is moved to compiler app
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
    if request.method == "POST":
        name = request.POST.get('roomname')  # name of element in form
        description = request.POST['description']

        username = request.user.get_username()
        host = User.objects.get(username=username)

        room_info = Room(host=host, name=name, description=description)
        room_info.save()

        if request.POST['btnradio'] == 'btnradio1':
            return redirect('createQuestion', room_info.id)
        else:
            msg = name + " room is created. Please wait for approval."
            messages.success(request, msg, extra_tags='info')
            return redirect('home')
    context = {}
    return render(request, "form2.html", context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        room = Room.objects.get(id=pk)
        room.name = request.POST.get('roomname')  # name of element in form
        room.description = request.POST['description']
        room.save()

        msg = room.name + " room successfully updated"
        messages.success(request, msg, extra_tags='warning')

        return redirect('home')

    context = {'room': room}
    return render(request, "form2.html", context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        room.delete()

        msg = room.name + " room successfully deleted"
        messages.success(request, msg, extra_tags='danger')

        return redirect('home')

    return render(request, "delete.html", {'obj': room})


@login_required(login_url='login')
def createQuestion(request, pk):
    if request.method == "POST":
        question_title = request.POST.get('questiontitle')
        question_full = request.POST['fullquestion']
        sample_test_case = request.POST['testcase']

        room = Room.objects.get(id=pk)

        question_info = Question(question_title=question_title, question_full=question_full,
                                 sample_test_case=sample_test_case, room=room)

        if request.POST['btnradio'] == 'btnradio1':
            question_info.save()
            return redirect('createQuestion', room.id)
        elif request.POST['btnradio'] == 'btnradio2':
            question_info.save()

            msg = " Question(s) added successfully "
            messages.success(request, msg, extra_tags='info')

            return redirect('room', room.id)
        else:
            return redirect('room', room.id)
    context = {}
    return render(request, "question_form2.html", context)


@login_required(login_url='login')
def updateQuestion(request, pk, pk2):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)
    # form = QuestionForm(instance=question)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        question = Question.objects.get(id=pk2)
        question.question_title = request.POST.get('questiontitle')
        question.question_full = request.POST['fullquestion']
        question.sample_test_case = request.POST['testcase']
        question.save()

        msg = " Question updated successfully "
        messages.success(request, msg, extra_tags='warning')

        return redirect('room', room.id)

    context = {'question': question}
    return render(request, "question_form2.html", context)


@login_required(login_url='login')
def deleteQuestion(request, pk, pk2):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        question.delete()

        msg = " Question deleted successfully "
        messages.success(request, msg, extra_tags='danger')

        return redirect('room', room.id)

    return render(request, "delete.html", {'obj': question})


# move to compiler-app
def finalSubmit(request):
    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
    context = {}
    return render(request, "submitted.html", context)


# responses related views
@login_required(login_url='login')
def roomResponses(request, pk):
    room = Room.objects.get(id=pk)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    solutions = Solution.objects.filter(room=room)

    context = {'solutions': solutions, 'room': room}
    return render(request, "responses.html", context)


@login_required(login_url='login')
def questionResponses(request, pk, pk2):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    solutions = Solution.objects.filter(question=question)

    context = {'solutions': solutions, 'room': room, 'question': question}
    return render(request, "responses.html", context)


# shifted to compiler-app
@login_required(login_url='login')
def viewResponses(request, pk, pk2, pk3):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)
    solution = Solution.objects.get(id=pk3)
    form = SolutionForm(instance=solution)
    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    context = {'form': form, 'question': question}
    return render(request, "view_response_question.html", context)


@login_required(login_url='login')
def deleteResponse(request, pk, pk2, pk3):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)
    solution = Solution.objects.get(id=pk3)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        solution.delete()
        msg = "Response of " + solution.user.username + " is successfully deleted"
        messages.success(request, msg, extra_tags='danger')
        return redirect('home')
    return render(request, "deleteResponse.html", {'obj': solution.user.username})


def unverifiedRooms(request):
    resultset = Room.objects.filter(verified=False)
    if request.user.username != "admin":
        return HttpResponse("You can't do this ...")

    context = {'rooms': resultset}
    return render(request, "unverified_rooms.html", context)


def approveRoom(request, pk):
    if request.user.username != "admin":
        return HttpResponse("You can't do this ...")

    room = Room.objects.get(id=pk)
    room.verified = True
    room.save()

    msg = " Room " + room.name + " by " + room.host.username + " is approved successfully."
    messages.success(request, msg, extra_tags='info')

    return redirect('unverifiedRooms')


def rejectRoom(request, pk):
    if request.user.username != "admin":
        return HttpResponse("You can't do this ...")

    room = Room.objects.get(id=pk)
    room.delete()

    msg = " Room " + room.name + " by " + room.host.username + " is rejected."
    messages.success(request, msg, extra_tags='danger')

    return redirect('unverifiedRooms')

