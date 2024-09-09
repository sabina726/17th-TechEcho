import json
from socket import timeout

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache
from django.template.loader import render_to_string

from .models import Notification


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return

        cache.set(f"notifications_user_{self.user.id}", self.channel_name, timeout=None)

        for q in self.user.follows.all():
            group_name = f"notifications_questions_{q.id}"
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
        for q in self.user.question_set.all():
            group_name = f"notifications_questions_{q.id}"
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

        self.accept()

    def disconnect(self, code):
        if self.user.is_authenticated and self.user.id == self.scope["user"].id:
            cache.delete(f"notifications_user_{self.user.id}")

            for q in self.user.follows.all():
                group_name = f"notifications_questions_{q.id}"
                async_to_sync(self.channel_layer.group_discard)(
                    group_name, self.channel_name
                )
            for q in self.user.question_set.all():
                group_name = f"notifications_questions_{q.id}"
                async_to_sync(self.channel_layer.group_discard)(
                    group_name, self.channel_name
                )

    def receive(self, text_data=None):
        if self.user.is_authenticated and self.user.id == self.scope["user"].id:
            self.user.notification_set.all().delete()

    def send_notification(self, event):
        message = event["message"]
        created_at = event["created_at"]

        html = render_to_string(
            "notifications/_new_notification.html",
            {
                "message": message,
                "created_at": created_at,
                "user": self.user,
            },
        )
        self.send(text_data=html)

    def leave_group(self, event):
        group_name = event["group_name"]
        async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)

    def join_group(self, event):
        group_name = event["group_name"]
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
