from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone


class TeacherInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    introduce = models.TextField(
        validators=[MinLengthValidator(150), MaxLengthValidator(500)]
    )
    nickname = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nickname or self.user.username} - {self.expertise}"
