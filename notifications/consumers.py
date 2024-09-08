from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = "notifications"
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )

    def send_model_notification(self, event):
        message = event["message"]
        print(message)
        self.send(text_data=message)

        # Send the message to the WebSocket
        # await self.send(text_data=json.dumps({
        #     'message': message
        # }))
