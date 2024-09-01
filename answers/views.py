from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from questions.models import Question
from answers.models import Answer

def index(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        answer = question.answer_set.create(content=request.POST["content"])
        return redirect("questions:show", id=id)

@csrf_exempt
def delete_answer(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, id=id)
        answer.delete()
        return redirect("questions:show", id=answer.question.id)