import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import QuestionForm
from .models import Question

# Create your views here.


def index(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        tags = request.POST.get("tags")

        # we require at least one tag
        if tags and form.is_valid():
            instance = form.save()
            tags = [tag["value"] for tag in json.loads(tags)]
            instance.tags.set(tags)
            instance.save()
            messages.success(request, "成功提問")
            return redirect("questions:index")

        messages.error(request, "輸入資料錯誤，請再嘗試")
        return render(request, "questions/new.html", {"form": form})
    questions = Question.objects.order_by("-votes_count")
    return render(request, "questions/index.html", {"questions": questions})


def new(request):
    form = QuestionForm()
    return render(request, "questions/new.html", {"form": form})


def show(request, id):
    question = get_object_or_404(Question, pk=id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        tags = request.POST.get("tags")
        # we require at least one tag
        if tags and form.is_valid():
            instance = form.save(commit=False)
            tags = [tag["value"] for tag in json.loads(tags)]
            instance.tags.set(tags)
            form.save_m2m()
            messages.success(request, "成功編輯")
            return redirect("questions:show", id=id)

        messages.error(request, "edit fail, retry")
        return render(
            request, "questions/edit.html", {"form": form, "question": question}
        )

    return render(
        request,
        "questions/show.html",
        {"question": question, "tags": question.tags.all()},
    )


def edit(request, id):
    question = get_object_or_404(Question, pk=id)
    form = QuestionForm(instance=question)
    return render(
        request,
        "questions/edit.html",
        {"form": form, "question": question, "tags": question.tags.all()},
    )


def delete(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        question.delete()
        return redirect("questions:index")


def upvotes(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        question.votes_count += 1
        question.save()
        return redirect("questions:show", id=id)


def downvotes(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        question.votes_count -= 1
        question.save()
        return redirect("questions:show", id=id)
