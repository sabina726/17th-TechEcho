from django.db import models
from django.contrib.auth.models import User

from questions.models import Question

from ckeditor.fields import RichTextField

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # upvotes = models.ManyToManyField(User, related_name="upvotes")
    # downvotes = models.ManyToManyField(User, related_name="downvotes")

    def __str__(self):
        return self.content
