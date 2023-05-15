from django.db import models
from django.conf import settings
import datetime

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lastAccessed = models.DateTimeField(auto_now=True)
    folder = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class Folder(models.Model):
    title = models.CharField(max_length=50)
    folder = models.IntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.title








