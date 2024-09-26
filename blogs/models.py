from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from taggit.managers import TaggableManager

User = get_user_model()


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
    likes = models.ManyToManyField(User, related_name="liked_blogs", blank=True)

    image = models.ImageField(
        upload_to="article_pictures/",
        null=True,
        blank=True,
        storage=S3Boto3Storage,
    )

    objects = BlogQuerySet.as_manager()
    labels = TaggableManager()

    def __str__(self):
        return self.title

    def publish(self):
        self.is_draft = False
        self.save()
        return self
