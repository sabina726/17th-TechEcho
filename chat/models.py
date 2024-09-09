from django.conf import settings
from django.db import models

from teachers.models import Teacher


# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.group_name}"


class GroupMessage(models.Model):
    group = models.ForeignKey(
        ChatGroup, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="messages", on_delete=models.CASCADE
    )
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.content}"

    class Meta:
        ordering = ["created_at"]
