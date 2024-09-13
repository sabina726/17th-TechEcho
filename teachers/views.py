from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from answers.models import Answer
from lib.utils.pagination import paginate
from questions.models import Question

from .forms import TeacherForm
from .models import Teacher


def mentor(request):
    return render(request, "teachers/mentor.html")


def index(request):
    if request.method == "POST":
        # 檢查是否該使用者已經是專家
        if Teacher.objects.filter(user=request.user).exists():
            messages.error(request, "你已經註冊為專家，無法重複註冊")
            return redirect("teachers:index")

        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher_info = form.save(commit=False)
            teacher_info.user = request.user
            teacher_info.save()
            messages.success(request, "歡迎加入")
            return redirect("teachers:index")

        return render(request, "teachers/new.html", {"form": form})

    teachers = Teacher.objects.all().order_by("-updated_at")
    teachers = paginate(request, teachers, items_count=8)
    return render(request, "teachers/index.html", {"teachers": teachers})


@login_required
def new(request):
    if request.user.is_teacher:
        messages.error(request, "你已經註冊為專家，無法重複註冊")
        return redirect("teachers:show", request.user.teacher.id)
    form = TeacherForm()
    return render(request, "teachers/new.html", {"form": form})


def show(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    chat_group = teacher.chat_group
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "更新成功")
            return redirect("teachers:show", id=id)
        return render(request, "teachers/edit.html", {"teacher": teacher, "form": form})

    questions = Question.objects.filter(user=teacher.user).order_by("-created_at")[:3]
    answers = (
        Answer.objects.filter(user=teacher.user)
        .select_related("question", "user")
        .order_by("-created_at")[:3]
    )
    context = {
        "teacher": teacher,
        "questions": questions,
        "answers": answers,
        "chat_group": chat_group,
    }

    return render(request, "teachers/show.html", context)


@login_required
def edit(request, id):
    teacher = get_object_or_404(Teacher, id=id, user=request.user)
    form = TeacherForm(instance=teacher)
    return render(request, "teachers/edit.html", {"teacher": teacher, "form": form})


@login_required
def delete(request, id):
    teacher = get_object_or_404(Teacher, id=id, user=request.user)
    teacher.delete()
    messages.success(request, "刪除成功")
    return redirect("teachers:index")
