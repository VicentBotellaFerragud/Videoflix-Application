from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length = 20)
    description = models.CharField(max_length = 400)
    created_at = models.DateField(default = date.today) 
    video_file = models.FileField(upload_to = 'videos')
    average_rating = models.IntegerField(default = 1, validators = [MinValueValidator(0), MaxValueValidator(5)])
    creator = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)])
    video = models.ForeignKey(Video, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.value)
