import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
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
        self.accept()

    def disconnect(self, code):
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


# class ChatroomConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user = self.scope["user"]
#         if not self.user.is_authenticated:
#             self.close()
#             return
#         self.chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
#         self.group = get_object_or_404(ChatGroup, id=self.chatroom_id)

#         async_to_sync(self.channel_layer.group_add)(
#             str(self.chatroom_id), self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         if self.user.is_authenticated and self.user.id == self.scope["user"].id:
#             async_to_sync(self.channel_layer.group_discard)(
#                 self.chatroom_name, self.channel_name
#             )

#     def receive(self, text_data=None):
#         if self.user.is_authenticated and self.user.id == self.scope["user"].id:
#             try:
#                 text_json = json.loads(text_data)
#                 content = text_json.get("content", "")
#                 if content:
#                     message = GroupMessage.objects.create(
#                         content=content, author=self.user, group=self.group
#                     )
#                     event = {"type": "message_handler", "message_id": message.id}
#                     async_to_sync(self.channel_layer.group_send)(
#                         self.chatroom_name, event
#                     )
#             except Exception:
#                 pass

#     def message_handler(self, event):
#         if self.user.is_authenticated and self.user.id == self.scope["user"].id:
#             message_id = event["message_id"]
#             message = GroupMessage.objects.get(pk=message_id)

#         text = render_to_string(
#             "chat/_message.html",
#             {"message": message, "user": self.user},
#         )
#         self.send(text_data=text)
