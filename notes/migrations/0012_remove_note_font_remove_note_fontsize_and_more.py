# Generated by Django 4.1.7 on 2023-12-22 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0011_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='font',
        ),
        migrations.RemoveField(
            model_name='note',
            name='fontSize',
        ),
        migrations.AddField(
            model_name='note',
            name='displayText',
            field=models.TextField(default='', max_length=5000),
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(max_length=8000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profilePicture',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='media/profile_pictures/'),
        ),
    ]
