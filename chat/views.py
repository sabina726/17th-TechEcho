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
