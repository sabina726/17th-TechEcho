from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BlogQuerySet(models.QuerySet):
    def drafts(self):
        return self.filter(is_draft=True)

    def published(self):
        return self.filter(is_draft=False)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blogs"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    views = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=True)

    objects = BlogQuerySet.as_manager()

    def __str__(self):
        return self.title
