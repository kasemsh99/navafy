# Generated by Django 4.1 on 2022-12-04 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0009_remove_media_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='profiles_avatar'),
        ),
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media_image'),
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ManyToManyField(related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
