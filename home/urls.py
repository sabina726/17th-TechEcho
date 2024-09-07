from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_view", views.search_view, name="search_view"),
]
