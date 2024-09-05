from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TeacherInfoForm
from .models import TeacherInfo


def index(request):
    if request.method == "POST":
        form = TeacherInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teachers:index")
        return render(request, "teachers/new.html", {"form": form})

    teachers = TeacherInfo.objects.all()
    teacher_data = [
        {
            "teacher": teacher,
            "questions": teacher.get_questions()[:3],
            "answers": teacher.get_answers()[:3],
        }
        for teacher in teachers
    ]

    context = {
        "teacher_data": teacher_data,
    }
    return render(request, "teachers/index.html", context)


def new(request):
    form = TeacherInfoForm()
    return render(request, "teachers/new.html", {"form": form})


def show(request, id):
    teacher = get_object_or_404(TeacherInfo, id=id)
    if request.method == "POST":
        form = TeacherInfoForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teachers:show", id)
        return render(request, "teachers/edit.html", {"teacher": teacher, "form": form})

    questions = teacher.get_questions()
    answered_questions = teacher.get_answers()
    context = {
        "teacher": teacher,
        "questions": questions,
        "answered_questions": answered_questions,
    }

    return render(request, "teachers/show.html", context)


def edit(request, id):
    teacher = get_object_or_404(TeacherInfo, id=id)
    form = TeacherInfoForm(instance=teacher)
    return render(request, "teachers/edit.html", {"teacher": teacher, "form": form})


def delete(request, id):
    teacher = get_object_or_404(TeacherInfo, id=id)
    teacher.delete()
    return redirect("teachers:index")
