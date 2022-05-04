from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from base.forms import SolutionForm
from base.models import Question


def question(request, pk, pk2):
    """
    For Submission
    """
    form = SolutionForm()
    # above one for form
    question = Question.objects.get(id=pk2)
    context = {'question': question, 'form': form}
    return render(request, "question.html", context)
