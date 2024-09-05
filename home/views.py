from django.contrib import messages
from django.shortcuts import render


def index(request):
    return render(request, "home/index.html")


def pages(request):
    messages.success(request, "登入成功！")
    return render(request, "home/pages.html", {"title": "登入", "content": "登入成功"})
