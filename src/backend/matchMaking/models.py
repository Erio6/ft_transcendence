from django.db import models
from user.models import UserProfile

# Create your models here.

class Match(models.Model):
    player_one = models.ForeignKey(UserProfile, related_name='player_one_match', on_delete=models.CASCADE)
    player_two = models.ForeignKey(UserProfile, related_name='player_two_match', null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('waiting', 'Waiting'), ('matched', 'Matched')], default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)


