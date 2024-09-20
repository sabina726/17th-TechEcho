from django.conf import settings
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_id = models.PositiveBigIntegerField(default=0)
    answer_id = models.PositiveBigIntegerField(default=0)
    message = models.TextField()
    url_name = models.CharField(max_length=100, null=True)
    clicked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
