from django.shortcuts import render


def nav(request):
    return render(request, "home/nav.html")  # dev


def index(request):
    return render(request, "home/index.html")


def pages(request):
    return render(request, "home/pages.html", {"title": "登入", "content": "登入成功"})
