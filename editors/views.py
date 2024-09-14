from django.shortcuts import render


def index(request):
    if request.POST:
        text = request.POST.get("text")
        language = request.POST.get("language")

    return render(request, "editors/index.html")
