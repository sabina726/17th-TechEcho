from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        context = {"user": request.user, "is_authenticated": True}
    else:
        context = {"is_authenticated": False}
    return render(request, "home/index.html", context)
