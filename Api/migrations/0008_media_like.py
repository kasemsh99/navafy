# Generated by Django 4.1 on 2022-11-22 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
