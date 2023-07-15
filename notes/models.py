from django.db import models
from django.conf import settings
import datetime

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lastAccessed = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, default=0)
    sharedUsers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sharedUsers')
    font = models.CharField(max_length=50, default='Helvetica')
    fontSize = models.IntegerField(default=16)

    def __str__(self):
        return self.title

class Folder(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('Folder', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class Preferances(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    backgroundImage = models.CharField(max_length=100, default='wavy')
    def __str__(self):
        return self.user.username








