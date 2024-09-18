from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from taggit.managers import TaggableManager

from chat.models import ChatGroup


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    labels = TaggableManager()
    introduce = models.TextField(
        validators=[MinLengthValidator(50), MaxLengthValidator(500)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chat_group = models.OneToOneField(
        "chat.ChatGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_teacher",
    )

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.user.is_teacher = True
            self.user.save()
            group_name = f"{self.user.username}"
            self.chat_group = ChatGroup.objects.create(group_name=group_name)
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.chat_group:
            self.chat_group.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}"
