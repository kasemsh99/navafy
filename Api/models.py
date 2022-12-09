from django.db import models
from django.contrib.auth.models import AbstractUser


class Artist(models.Model):
    country = models.CharField(max_length=150, null=True, blank=True)
    genre = models.CharField(max_length=150, null=True, blank=True)
    user = models.OneToOneField('Api.CustomUser', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)



class Favorite(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    medias = models.ManyToManyField(Media, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return f'user {self.user} Comment on {self.media}'


class Post(models.Model):
    title = models.CharField(max_length=50)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    media = models.OneToOneField(Media, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'user {self.user} post {self.media}'

class Media(models.Model):
    title = models.CharField(max_length=50)
    type = models.IntegerField(choices=[(1, 'Music'), (2, 'Music Video'), (3, 'Book')], default=1)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media_image', null=True, blank=True)
    genre = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='media_like', blank=True)

    def __str__(self):
        return self.title
