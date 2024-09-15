from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import ChatGroup

from .forms.chat_form import ChatMessageForm


# Create your views here.
@login_required
def index(request):
    chat_groups = ChatGroup.objects.all()
    return render(request, "chat/index.html", {"chat_groups": chat_groups})


@login_required
def room(request, id):
    chat_group = get_object_or_404(ChatGroup, pk=id)

    # redirect intruders to the teachers show page
    # while sending them an error message saying they are not allowed to join without a reservation/appointment
    if not chat_group.has_member(request.user):
        messages.error(
            request,
            "您沒有權限進入這個聊天室。",
        )
        return redirect("appointments:appointment")

    chat_messages = chat_group.messages.all()[:30]
    other_user = chat_group.members.exclude(pk=request.user.id).first()
    form = ChatMessageForm()

    return render(
        request,
        "chat/chat.html",
        {
            "chat_messages": chat_messages,
            "form": form,
            "chat_group": chat_group,
            "other_user": other_user,
        },
    )
