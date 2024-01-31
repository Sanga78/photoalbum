from django.db import models
from users.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Album(models.Model):
    album_title = models.CharField(max_length=100)
    date_created = models.DateField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.album_title
    
    def get_absolute_url(self):
        return reverse('album-detail', kwargs={'pk': self.pk})

class Photo(models.Model):
    photo_title = models.CharField(max_length=100)
    album_id = models.ForeignKey(Album,on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return self.photo_title