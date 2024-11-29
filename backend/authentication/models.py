from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField( default='avatar/default.jpg',upload_to='avatar')
    friends = models.ManyToManyField('self',blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    match_history = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'