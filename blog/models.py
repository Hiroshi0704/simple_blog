from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse

class Post(models.Model):
    title       = models.CharField(max_length=225)
    body        = models.TextField()
    create_at   = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now=True)
    author      = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

class Comment(models.Model):
    comment     = models.CharField(max_length=140)
    create_at   = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now=True)
    author      = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post        = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment