from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("teachers/", include("teachers.urls")),
    path("questions/", include("questions.urls")),
    path("users/", include("users.urls")),
    path("questions/<int:id>/answers/", include("answers.urls")),
    path("payments/", include("payments.urls")),
    path("accounts/", include("allauth.urls")),
    path("chat/", include("chat.urls")),
    path("reservations/", include("reservations.urls")),
    path("blogs/", include("blogs.urls")),
]


def custom_404(request, exception):
    return redirect("http://10.8.8.93:5173/test_vue/404-page")


handler404 = custom_404
