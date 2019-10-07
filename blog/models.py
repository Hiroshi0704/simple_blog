from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

class Post(models.Model):
    title       = models.CharField(max_length=225)
    body        = models.TextField()
    create_at   = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now=True)
    author      = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    def get_create_at(self):
        return self.create_at.strftime('%Y-%m-%d %H:%M:%S')

    def is_current(self):
        now = timezone.now()
        passed_date = now - timezone.timedelta(days=3)
        return self.create_at > passed_date

class Comment(models.Model):
    comment     = models.CharField(max_length=140)
    create_at   = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now=True)
    author      = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post        = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_at']

    def __str__(self):
        return self.comment

