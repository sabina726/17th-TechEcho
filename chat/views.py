from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import ChatGroup
from lib.utils.pagination import paginate

from .forms.chat_form import ChatMessageForm


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

    chat_messages = chat_group.messages.select_related("author")
    if request.htmx:
        chat_messages = paginate(request, chat_messages, items_count=30)
        return render(
            request,
            "chat/partials/_message_list.html",
            {"chat_messages": chat_messages, "chat_group_id": chat_group.id},
        )

    chat_messages = paginate(request, chat_messages, items_count=30, default_page=-1)
    return render(
        request,
        "chat/chat.html",
        {
            "chat_messages": chat_messages,
            "form": ChatMessageForm(),
            "chat_group": chat_group,
            "other_user": chat_group.get_other_user(request.user),
            "online_count": chat_group.members_online.count(),
        },
    )
