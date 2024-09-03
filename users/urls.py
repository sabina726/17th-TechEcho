from django.urls import include, path

from . import views

app_name = "users"

urlpatterns = [
    path("<slug:slug>/login/", views.log_in, name="login"),
    path("login/", views.log_in, name="login_no_id"),
    path("logout/", views.log_out, name="log_out"),
    path("register/", views.register, name="register"),
    path("register/", views.register, name="register_no_id"),
    path("users/<slug:slug>member", views.profile, name="profile"),
]
