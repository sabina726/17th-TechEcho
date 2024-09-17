# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/editor/<str:room_name>/', consumers.CollaborativeEditorConsumer.as_asgi()),
]
