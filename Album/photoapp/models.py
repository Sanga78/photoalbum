from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()

class Album(models.Model):
    album_title = models.CharField(max_length = 17)
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)

class Photo(models.Model):
    album_id = models.ForeignKey(Album,on_delete=models.CASCADE)
    photo_title = models.CharField(max_length = 25)
    image_url = models.URLField()
