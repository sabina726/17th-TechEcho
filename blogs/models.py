from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager


class BlogQuerySet(models.QuerySet):
    def drafts(self):
        return self.filter(is_draft=True)

    def published(self):
        return self.filter(is_draft=False)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blogs"
    )
    views = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=True)

    objects = BlogQuerySet.as_manager()
    labels = TaggableManager()

    def __str__(self):
        return self.title

    def publish(self):
        self.is_draft = False
        self.save()
        return self
