from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='following')
    avatar = models.ImageField(default='users/default_avatar.png', upload_to='users', blank=True)
    location = models.CharField(default="No location provided", max_length=100, blank=True)
    bio = models.TextField(default="Nothing to say...", max_length=140, blank=True)

    def get_absolute_url(self):
        return reverse("profile_detail", args=[self.pk])

    def following_posts(self):
        return self.following.all()

    def __str__(self):
        return f'{self.user.username}'

class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='posts' ,on_delete=models.CASCADE)
    message = models.TextField(max_length=350)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Profile, related_name="likes", blank=True)

    def __str__(self):
        return f'{self.author} - {self.message[:25]}'

    class Meta:
        ordering = ('-created', )

    def serialize(self):
        return {
            'id': self.id,
            'author': self.author.user.username,
            "message": self.message,
            "likes": [author.user.username for author in self.likes.all()]
        }


    


