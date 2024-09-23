import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from chat.models import ChatGroup, GroupMessage


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        self.chat_group = get_object_or_404(ChatGroup, id=chatroom_id)
        self.group_name = f"chatroom_{chatroom_id}"
        self.is_public = self.chat_group.is_public
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        if not self.chat_group.members_online.filter(pk=self.user.id).exists():
            self.chat_group.members_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, code):
        if self.chat_group.members_online.filter(pk=self.user.id).exists():
            self.chat_group.members_online.remove(self.user)
            self.update_online_count()

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data):
        text_json = json.loads(text_data)
        content = text_json.get("content", "").strip()
        if content:
            message = GroupMessage.objects.create(
                content=content, author=self.user, group=self.chat_group
            )
            event = {"type": "message_handler", "message_id": message.id}
            async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def message_handler(self, event):
        message_id = event["message_id"]
        message = GroupMessage.objects.get(pk=message_id)

        text = render_to_string(
            "chat/partials/_message.html",
            {"message": message, "user": self.user},
        )
        self.send(text_data=text)

    def update_online_count(self):
        online_count = self.chat_group.members_online.count()
        if self.is_public:
            event = {"type": "online_count_handler", "online_count": online_count}
        else:
            event = {
                "type": "online_status_handler",
                "online_count": online_count,
            }

        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def online_status_handler(self, event):
        text = render_to_string(
            "chat/partials/_online_status.html",
            {
                "online_count": event["online_count"],
                "other_user": self.chat_group.get_other_user(self.user),
            },
        )

        self.send(text_data=text)

    def online_count_handler(self, event):
        text = render_to_string(
            "chat/partials/_online_count.html",
            {
                "online_count": event["online_count"],
            },
        )

        self.send(text_data=text)
