from django.shortcuts import render


def index(request):
    return render(request, "home/index.html")


def nav(request):
    return render(request, "home/nav.html")  # 開發用


def pages(request):
    return render(request, "home/pages.html", {"title": "登入", "content": "登入成功"})
