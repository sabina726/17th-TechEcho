from django.urls import path
from . import views

app_name = "answers"

urlpatterns = [
    path("", views.index, name="index"),
    path("delete", views.delete_answer, name="delete_answer"),
    path("upvote", views.upvote_answer, name="upvote_answer"),
    path("downvote", views.downvote_answer, name="downvote_answer"),
]