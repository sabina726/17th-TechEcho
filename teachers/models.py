from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone

from users.models import Users


class TeacherInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    introduce = models.TextField(
        validators=[MinLengthValidator(150), MaxLengthValidator(500)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.expertise}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        user_profile = Users.objects.filter(member=self.user).first()
        if user_profile:
            user_profile.is_teacher = True
            user_profile.save()
