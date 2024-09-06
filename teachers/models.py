from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from answers.models import Answer
from questions.models import Question

TIME_SLOTS = [
    ("09:00-10:00", "09:00 - 10:00 AM"),
    ("10:00-11:00", "10:00 - 11:00 AM"),
    ("11:00-12:00", "11:00 - 12:00 PM"),
    # Add more time slots as needed
]


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    introduce = models.TextField(
        validators=[MinLengthValidator(100), MaxLengthValidator(500)]
    )
    nickname = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule = models.TextField(
        max_length=20, choices=TIME_SLOTS, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_teacher = True
            self.user.save()
        super().save(*args, **kwargs)

    def get_questions(self):
        return Question.objects.filter(user=self.user)

    def get_answers(self):
        return Answer.objects.filter(user=self.user)
