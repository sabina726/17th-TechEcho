from django.urls import path

from . import views

app_name = "editors"

urlpatterns = [path("", views.index, name="index")]
