from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    # there must be a better regex that fits both in one
    path("ws/notifications/", consumers.NotificationConsumer.as_asgi()),
    re_path(r"^.*/ws/notifications/$", consumers.NotificationConsumer.as_asgi()),
]
