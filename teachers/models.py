import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone

from answers.models import Answer
from chat.models import ChatGroup
from questions.models import Question


def verify(value):
    # 正則表達式：允許中文字符、英文字符和空格
    if not re.match(r"^[\u4e00-\u9fffA-Za-z\s]*$", value):
        raise ValidationError("專業能力只能包含中英文字符")


def generate_unique_group_name(base_name):
    """Generates a unique group name by appending a number if necessary."""
    group_name = base_name
    counter = 1
    while ChatGroup.objects.filter(group_name=group_name).exists():
        group_name = f"{base_name}-{counter}"
        counter += 1
    return group_name


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255, validators=[verify])
    introduce = models.TextField(
        validators=[MinLengthValidator(50), MaxLengthValidator(500)]
    )
    nickname = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule_start = models.DateTimeField(default=timezone.now)
    schedule_end = models.DateTimeField(null=True, blank=True)
    chat_group = models.OneToOneField(
        "chat.ChatGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_teacher",
    )

    def save(self, *args, **kwargs):
        # 如果是新紀錄，則設定 user 為 teacher 並保存
        if not self.pk:
            super().save(*args, **kwargs)
            self.user.is_teacher = True
            self.user.save()

        # 如果沒有 chat_group，則創建一個新的群組
        if not self.chat_group:
            base_name = self.nickname or self.user.username
            unique_group_name = generate_unique_group_name(base_name)
            chat_group = ChatGroup.objects.create(group_name=unique_group_name)
            self.chat_group = chat_group
            self.chat_group.save()
        # 不再更新已存在的 chat_group 名稱
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.expertise}"

    def get_questions(self):
        return Question.objects.filter(user=self.user)

    def get_answers(self):
        return Answer.objects.filter(user=self.user)
