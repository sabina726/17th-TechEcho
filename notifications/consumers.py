from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return

        self.GROUP_NAME = "notifications"
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)

        self.accept()

    def disconnect(self, code):
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.GROUP_NAME, self.channel_name
            )

    def send_notification(self, event):
        message = event["message"]
        html = render_to_string(
            "notifications/_notification.html", {"message": message, "user": self.user}
        )
        self.send(text_data=html)
