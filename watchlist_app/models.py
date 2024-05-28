from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
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
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Reviews(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    descritpion = models.CharField(max_length=192)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # for fake reviews
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title



