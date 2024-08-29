from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone


class TeacherInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 連接User模型
    expertise = models.CharField(max_length=255)  # 專業能力
    introduce = models.TextField(
        validators=[MinLengthValidator(150), MaxLengthValidator(500)]
    )  # 簡單自傳，長度限制
    created_at = models.DateTimeField(default=timezone.now)  # 新增時間
    def __str__(self):
        return f"{self.user.username} - {self.expertise}"
