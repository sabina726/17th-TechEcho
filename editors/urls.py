from django.urls import path

from . import views

app_name = "editos"

urlpatterns = [path("", views.index, name="index")]
