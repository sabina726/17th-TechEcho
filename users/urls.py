from django.urls import include, path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="log_out"),
    path("register/", views.register, name="register"),
    path("register/", views.register, name="register_no_id"),
    path("users/<slug:slug>member", views.profile, name="profile"),
]
