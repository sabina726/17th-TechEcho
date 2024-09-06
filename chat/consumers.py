from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from chat.models import ChatGroup, GroupMessage
import json
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.group = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        # self.channel_name is auto genearted by channels
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        
        self.accept()

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )


    def receive(self, text_data=None):
        text_json = json.loads(text_data)
        content = text_json['content']
        
        message = GroupMessage.objects.create(
            content = content, 
            author = self.user,
            group = self.group
        )
        event = {
            "type": "message_handler",
            "message_id": message.id
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
       

    # a method automatically called every turn a message is sent to clients
    # this is an event handler
    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(pk=message_id)

        text = render_to_string("chat/_message.html", {
            'chat_message': message,
            'user': self.user
        })
        self.send(text_data=text)