from django.contrib import admin
from .models import Note, Folder

# Register your models here.

admin.site.register(Note)
admin.site.register(Folder)