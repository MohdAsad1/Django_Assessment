from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_articles')
    dislikes = models.ManyToManyField(User, related_name='disliked_articles')
    time = models.DateTimeField(auto_now_add=True, blank=True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True, blank=True ,null=True)

