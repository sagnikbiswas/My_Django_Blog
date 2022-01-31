from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from .validators import validate_tags

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(validators=[validate_tags])
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class About(models.Model):
    html_content = models.TextField()

    def get_absolute_url(self):
        return reverse('blog_about')