# routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/editor/<int:editor_id>/", consumers.CollaborativeEditorConsumer.as_asgi()),
]
