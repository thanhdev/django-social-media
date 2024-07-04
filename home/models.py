from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property


class User(AbstractUser):
    avatar = models.ImageField(upload_to="user-avatars/", blank=True)
    bio = models.TextField(blank=True)
    REQUIRED_FIELDS = []

    @cached_property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f"https://ui-avatars.com/api/?name={self.username}"


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    class Meta:
        ordering = ("-created_at",)
