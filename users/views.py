from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import User


def register(request, id=None):
    if id:
        existing_user = get_object_or_404(User, pk=id)
    else:
        existing_user = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if not username or not password:
            messages.error(request, "必須填寫帳號跟密碼")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "此用戶名已存在")
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email, name=username
            )
            messages.success(request, "註冊成功")
            return redirect("users:login")

    return render(request, "register.html", {"existing_user": existing_user})


def log_in(request, id=None):
    if id:
        existing_user = get_object_or_404(User, pk=id)
    else:
        existing_user = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("pages")
        else:
            messages.error(request, "登入失敗：用戶名或密碼不正確")

    return render(request, "login.html", {"existing_user": existing_user})


def profile(request, id):
    return render(request, "users/profile.html")


def log_out(request):
    logout(request)
    messages.success(request, "登出成功")
    return redirect("index")
