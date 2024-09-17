from channels.generic.websocket import AsyncWebsocketConsumer

class CollaborativeEditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'editor_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, bytes_data):
        # Broadcast the change to the other clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'editor_message',
                'bytes_data': bytes_data
            }
        )

    async def editor_message(self, event):
        # Send message to WebSocket
        await self.send(bytes_data=event['bytes_data'])
