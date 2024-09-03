from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

User = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
