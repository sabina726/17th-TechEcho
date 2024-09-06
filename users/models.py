from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    third_party = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
