from channels.generic.websocket import AsyncWebsocketConsumer


class CollaborativeEditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.editor_id = self.scope["url_route"]["kwargs"]["editor_id"]
        self.room_group_name = f"editor_{self.editor_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, bytes_data):
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "editor_message", "bytes_data": bytes_data}
        )

    async def editor_message(self, event):
        await self.send(bytes_data=event["bytes_data"])
