from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager


class EditorGroup(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.TextField()
    language = TaggableManager()
