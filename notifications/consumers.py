import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string

from .models import Notification


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return

        for q in self.user.follows.all():
            group_name = f"notifications_questions_{q.id}"
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
        for q in self.user.question_set.all():
            group_name = f"notifications_questions_{q.id}"
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

        self.accept()

    def disconnect(self, code):
        if self.user.is_authenticated and self.user.id == self.scope["user"].id:
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
        if self.user.is_authenticated and self.user.id == self.scope["user"].id:
            message = event["message"]
            # save the news in db
            Notification.objects.create(user=self.user, message=message)

            html = render_to_string(
                "notifications/_new_notification.html",
                {"message": message, "user": self.user},
            )
            self.send(text_data=html)
