from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("",views.index, name="index"),
    # should be an incomprehensible hash
    path("<int:id>", views.room, name="room")
]
