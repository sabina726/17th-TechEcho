from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    third_party = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(5)}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
