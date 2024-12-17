from django.contrib.auth.models import User
from django.db import models
from user.models import UserProfile

# Create your models here.
class Game(models.Model):
    player_one = models.ForeignKey(UserProfile, related_name='player_one_games', on_delete=models.CASCADE)
    player_two = models.ForeignKey(UserProfile, related_name='player_two_games', on_delete=models.CASCADE)
    winner = models.ForeignKey(UserProfile, related_name='winner_games', null=True, on_delete=models.SET_NULL)
    looser = models.ForeignKey(UserProfile, related_name='looser_games',null=True, on_delete=models.SET_NULL)
    player_one_score = models.IntegerField(default=0, null=True, blank=True)
    player_two_score = models.IntegerField(default=0, null=True, blank=True)
    winner_score = models.IntegerField(default=0, null=True, blank=True)
    looser_score = models.IntegerField(default=0, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player_one.display_name} vs {self.player_two.display_name}'

class SoloGame(models.Model):
    player_solo = models.ForeignKey(UserProfile, related_name='player_one_games_solo', on_delete=models.CASCADE)
    winner = models.ForeignKey(UserProfile, related_name='winner_games_solo', null=True, on_delete=models.CASCADE)
    looser = models.ForeignKey(UserProfile, related_name='looser_games_solo',null=True, on_delete=models.CASCADE)
    player_solo_score = models.IntegerField(default=0)
    IA_score = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)


