import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from base.forms import SolutionForm
from base.models import Question, Room, Solution


def question(request, pk, pk2):
    question = Question.objects.get(id=pk2)
    submitFlag = True
    context = {'question': question,'submitFlag':submitFlag}
    return render(request, "question.html", context)


def runCode(request, pk, pk2):
    if request.method == 'POST':
        code = request.POST['code']
        input = request.POST['input']
        y = input
        input_part = input.replace("\n", " ").split(" ")

        def input():
            a = input_part[0]
            del input_part[0]
            return a

        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code)
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = e
        print(output)
    submitFlag = True
    question = Question.objects.get(id=pk2)
    context = {'question': question, "code": code, "input": y, "output": output,'submitFlag':submitFlag }
    return render(request, 'question.html', context)


def finalSubmit(request,pk,pk2):
    if request.method == "POST":
        code = request.POST['code']
        input = request.POST['input']
        username = request.user.get_username()
        user = User.objects.get(username=username)
        question =Question.objects.get(id=pk2)
        room= Room.objects.get(id=pk)

        sol_info = Solution(code=code,user=user,question=question,room=room,input=input)
        sol_info.save()

    context = {}
    return render(request, "submitted.html", context)


@login_required(login_url='login')
def viewResponses(request, pk, pk2, pk3):
    question = Question.objects.get(id=pk2)
    solution = Solution.objects.get(id=pk3)
    code = solution.code
    if solution.input == None:
        input = ""
    else:
        input = solution.input
    output = ""
    submitFlag=False
    context = {'question': question, "code": code, "input": input, 'output': output,'submitFlag':submitFlag }
    return render(request, 'question.html', context)


def runResponse(request, pk, pk2, pk3):
    if request.method == 'POST':
        code = request.POST['code']
        input = request.POST['input']
        y = input
        input_part = input.replace("\n", " ").split(" ")

        def input():
            a = input_part[0]
            del input_part[0]
            return a

        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code)
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = e
        print(output)

    question = Question.objects.get(id=pk2)
    context = {'question': question, "code": code, "input": y, "output": output}
    return render(request, 'question.html', context)
