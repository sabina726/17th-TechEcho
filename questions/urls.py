from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/edit/", views.edit, name="edit"),
    path("<int:id>/delete/", views.delete, name="delete"),
    path("<int:id>/votes/", views.votes, name="votes"),
    path("<int:id>/follows/", views.follows, name="follows"),
    path("<int:id>/", views.show, name="show"),
    path("new/", views.new, name="new"),
    path("preview/", views.preview, name="preview"),
]
