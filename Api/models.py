from django.db import models
from django.contrib.auth.models import AbstractUser

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