# routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/editor/collab/<int:collab_id>/", consumers.CollabConsumer.as_asgi()),
    path("ws/editor/result/<int:result_id>/", consumers.ResultConsumer.as_asgi()),
]
