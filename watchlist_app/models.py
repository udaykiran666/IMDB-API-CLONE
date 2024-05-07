from django.db import models

# Create your models here.

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=64)
    about = models.CharField(max_length=192)
    website = models.URLField(max_length=192)


    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=64)
    storyline = models.CharField(max_length=192)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title