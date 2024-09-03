from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    # Customize the admin interface as needed


admin.site.register(User, CustomUserAdmin)
