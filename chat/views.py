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
    if chat_group.has_member(request.user):
        messages.error(
            request,
            "這位老師沒有把您加入這個聊天室，或許您沒有預約，或是老師有所疏漏。假如您已經有預約，請稍候幾分鐘再嘗試。",
        )
        return redirect("teachers:show", id=chat_group.assigned_teacher.id)

    chat_messages = chat_group.messages.all()[:30]

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return redirect("chat:room", id=id)

    form = ChatMessageForm()

    return render(
        request,
        "chat/chat.html",
        {
            "chat_messages": chat_messages,
            "form": form,
            "room_id": id,
            "chat_group": chat_group,
        },
    )
