from django.db import models
from django.conf import settings
import datetime

# Create your models here.


"""
Notes - 
    title - the title of the note 
    text - the contents of the note
    owner - the user who created the note
    lastAccessed - the last time the note was opened
    folder - the folder the note is in, defaults to the main root folder of the user
    sharedUsers - the users the note is shared with
    font - the font of the note
    fontSize - the size of the font
"""
class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=8000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lastAccessed = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, default=0)
    sharedUsers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sharedUsers')
    displayText = models.TextField(max_length=5000, default='')

    def __str__(self):
        return self.title


"""
Folder -
    title - the title of the folder
    parent - the folder this folder is in, defaults to the main root folder of the user
    owner - the user who created the folder
    home - if this folder is the main root folder of the user. True if it is the main root folder of the user
"""
class Folder(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('Folder', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home = models.BooleanField(default=False)
    def __str__(self):
        return self.title



"""Preferances of the user"""
class Preferances(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    backgroundImage = models.CharField(max_length=100, default='wavy')
    def __str__(self):
        return self.user.username


"""The user's profile"""
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profilePicture = models.ImageField(upload_to='media/profile_pictures/', blank=True, null=True)
    def __str__(self):
        return self.user.username







