from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# from .form import ChatMessageForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import ChatGroup


# Create your views here.
def index(request):
    if request.method == "POST":
        pass
        ChatGroup.objects.create(
            group_name="test",
        )

    return render(request, "chat/index.html")


# @login_required
def room(request, id):
    chat_group = get_object_or_404(ChatGroup, group_name="test")
    return HttpResponse("testing")
