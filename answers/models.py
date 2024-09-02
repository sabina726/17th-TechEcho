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

    upvote = models.ManyToManyField(User, related_name="upvote_answer")
    downvote = models.ManyToManyField(User, related_name="downupvote_answer")
    votes_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.content

    # votes = models.IntegerField(default=0)
    # total_votes = models.IntegerField(default=0)

# class Vote(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     vote_type = models.CharField(max_length=10, choices=[("upvote", "Upvote"), ("downvote", "ownvote")])

#     class Meta:
#         unique_together = ("user", "answer")
