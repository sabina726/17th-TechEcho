from django.shortcuts import render


def index(request):
    if request.POST:
        text = request.POST.get("text")
        print(text)

    return render(request, "editors/index.html")
