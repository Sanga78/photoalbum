from django.db import models
from django.utils import timezone
from PIL import Image

# Create your models here.
            
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Album(models.Model):
    album_title = models.CharField(max_length=100)
    date_created = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.album_title


class Photo(models.Model):
    photo_title = models.CharField(max_length=100)
    album_id = models.ForeignKey(Album,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='photos')

    def __str__(self):
        return self.photo_title
    
def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
