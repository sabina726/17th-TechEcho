import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CollabConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.collab_id = self.scope["url_route"]["kwargs"]["collab_id"]
        self.group_name = f"collab_{self.collab_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, bytes_data):
        print("hi")
        await self.channel_layer.group_send(
            self.group_name, {"type": "editor_message", "bytes_data": bytes_data}
        )

    async def editor_message(self, event):
        await self.send(bytes_data=event["bytes_data"])


class ResultConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.result_id = self.scope["url_route"]["kwargs"]["result_id"]
        self.group_name = f"result_{self.result_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_json = json.loads(text_data)
        event = {
            "type": "result_message",
            "language": text_json.get("language", ""),
            "code": text_json.get("code", ""),
        }
        await self.channel_layer.group_send(self.group_name, event)

    async def result_message(self, event):
        await self.send(text_data=event["code"])
