import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from chat.models import ChatGroup, GroupMessage


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        self.group = get_object_or_404(ChatGroup, id=self.chatroom_id)

        async_to_sync(self.channel_layer.group_add)(
            str(self.chatroom_id), self.channel_name
        )

        event = {"type": "update_members_online", "change": 1}
        async_to_sync(self.channel_layer.group_send)(str(self.chatroom_id), event)
        self.accept()

    def disconnect(self, code):
        event = {"type": "update_members_online", "change": -1}
        async_to_sync(self.channel_layer.group_send)(str(self.chatroom_id), event)

        async_to_sync(self.channel_layer.group_discard)(
            str(self.chatroom_id), self.channel_name
        )

    def receive(self, text_data):
        text_json = json.loads(text_data)
        content = text_json.get("content", "").strip()
        if content:
            message = GroupMessage.objects.create(
                content=content, author=self.user, group=self.group
            )
            event = {"type": "message_handler", "message_id": message.id}
            async_to_sync(self.channel_layer.group_send)(str(self.chatroom_id), event)

    def message_handler(self, event):
        message_id = event["message_id"]
        message = GroupMessage.objects.get(pk=message_id)

        text = render_to_string(
            "chat/_message.html",
            {"message": message, "user": self.user},
        )
        self.send(text_data=text)

    def update_members_online(self, event):
        change = event["change"]
        self.group.members_online = F("members_online") + change
        self.group.save()

        text = render_to_string(
            "chat/_online_status.html",
        )
