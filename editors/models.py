from django.conf import settings
from django.db import models


class EditorGroup(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(default="javascript")
    chooser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="editor_language_choice",
        on_delete=models.SET_NULL,
        null=True,
    )
