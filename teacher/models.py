from django.contrib.auth.models import User
from django.core.validators import (EmailValidator, MaxLengthValidator,
                                    MinLengthValidator)
from django.db import models
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=255)  # 學生姓名
    email = models.EmailField(validators=[EmailValidator()])  # 學生信箱

    def __str__(self):
        return self.name


class TeacherInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 連接User模型
    expertise = models.CharField(max_length=255)  # 專業能力
    introduce = models.TextField(
        validators=[MinLengthValidator(150), MaxLengthValidator(500)]
    )  # 簡單自傳，長度限制
    students = models.ManyToManyField(Student, related_name="teachers")
    created_at = models.DateTimeField(default=timezone.now)  # 新增時間

    def __str__(self):
        return f"{self.user.username} - {self.expertise}"
