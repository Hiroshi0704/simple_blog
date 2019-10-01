import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

import random
from faker import Faker
from blog.models import Post, Comment
from django.contrib.auth import get_user_model

fakergen = Faker()


def create_user_model(num):
    user = get_user_model()

    for i in range(num):
        username = fakergen.name()
        email = fakergen.email()
        password = 'test12345'
        user.objects.get_or_create(username=username, email=email, password=password)


def create_post_model(num):
    user = get_user_model()

    for i in range(num):
        title = fakergen.word()
        body = fakergen.text()
        author = random.choice(user.objects.all())
        Post.objects.get_or_create(title=title, body=body, author=author)

def create_comment_model(num):
    user = get_user_model()

    for i in range(num):
        comment = fakergen.text()
        author = random.choice(user.objects.all())
        post = random.choice(Post.objects.all())
        Comment.objects.get_or_create(comment=comment, author=author, post=post)

if __name__ == '__main__':
    create_user_model(20)
    create_post_model(20)
    create_comment_model(100)
    