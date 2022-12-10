# Generated by Django 4.1 on 2022-12-04 05:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0011_remove_media_like_media_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='media_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
