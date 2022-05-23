from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EventPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, blank=True, related_name="participants")

    title = models.CharField(max_length=75)
    content = models.TextField(max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'