from django.shortcuts import get_object_or_404, redirect, render

from .forms import TeacherInfoForm
from .models import TeacherInfo


def index(request):
    return render(request, "teacher/index.html")


def new(request):
    return render(request, "teacher/new.html")


def show(request, id):
    return render(request, "teacher/show.html")


def edit(request, pk):
    return render(request, "teacher/edit.html")


def delete(request):
    return redirect("teacher:index")
