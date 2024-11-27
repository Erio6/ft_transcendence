from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='media/', blank=True, null=True, default='media/chat.jpg')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', blank=True)
    match_history = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.user.username