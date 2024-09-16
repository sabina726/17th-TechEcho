from django.conf import settings
from django.db import models


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chat_group", blank=True
    )
    members_online = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="online_group", blank=True
    )

    def get_other_user(self, user):
        return self.members.exclude(pk=user.id).first()

    def has_member(self, user):
        # temporarily
        if getattr(self.assigned_teacher, "user", None) == user:
            self.members.add(self.assigned_teacher.user)

        return self.members.filter(pk=user.id).exists()

    def __str__(self):
        return f"{self.group_name} by {self.assigned_teacher if self.assigned_teacher else 'Unknown Teacher'}"


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
