from django.shortcuts import get_object_or_404, redirect, render

from .forms import TeacherInfoForm
from .models import TeacherInfo


def index(request):
    if request.method == "POST":
        form = TeacherInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher:index")
        return render(request, "teachers/new.html", {"form": form})

    teachers = TeacherInfo.objects.all()
    return render(request, "teachers/index.html", {"teachers": teachers})


def new(request):
    form = TeacherInfoForm()
    return render(request, "teachers/new.html", {"form": form})


def show(request, id):
    teacher = get_object_or_404(TeacherInfo, id=id)
    if request.method == "POST":
        form = TeacherInfoForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teacher:show", id)
        return render(request, "teachers/new.html", {"form": form})

    return render(request, "teachers/show.html", {"teacher": teacher})


def edit(request, id):
    teacher = get_object_or_404(TeacherInfo, id=id)
    form = TeacherInfoForm(instance=teacher)
    return render(request, "teachers/edit.html", {"teacher": teacher, "form": form})


def delete(request, id):
    teacher = get_object_or_404(TeacherInfo, id=id)
    teacher.delete()
    return redirect("teacher:index")
