import os.path
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField( default='avatar/default.jpg',upload_to='avatar')
    display_name = models.CharField(max_length=100, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    match_history = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar and os.path.exists(self.avatar.path):
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    def __str__(self):
        return f'{self.user.username} Profile'
# Create your models here.
