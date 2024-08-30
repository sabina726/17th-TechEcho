from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone


class TeacherInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    introduce = models.TextField(
        validators=[MinLengthValidator(150), MaxLengthValidator(500)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.expertise}"
