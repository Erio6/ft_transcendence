from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    #pseudo = models.TextField(null=True, blank=True)
    friends_number = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username