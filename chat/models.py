from django.db import models
from django.conf import settings
from teachers.models import TeacherInfo

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100 ,unique=True)
    teacher = models.OneToOneField(TeacherInfo, on_delete=models.CASCADE)

    def __str__(self):
        # should be f"{self.group_name} by {self.teacher.nickname}" with TeacherInfo model updated in the future
        return f"{self.group_name}"


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, realated_name="messages", on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.content}"


    class Meta:
        ordering = ['created']