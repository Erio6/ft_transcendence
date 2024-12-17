from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Game(models.Model):
    player_one = models.ForeignKey(User, related_name='player_one', on_delete=models.CASCADE)
    player_two = models.ForeignKey(User, related_name='player_two', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='winner', null=True, on_delete=models.CASCADE)
    looser = models.ForeignKey(User, related_name='looser',null=True, on_delete=models.CASCADE)
    player_one_score = models.IntegerField(default=0)
    player_two_score = models.IntegerField(default=0)
    winner_score = models.IntegerField(default=0)
    looser_score = models.IntegerField(default=0)
    #score = models.JSONField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)


"""
Game Solo
-player (pseudo, avatar, rank)
-register player in Bool
-guest ID if not register 
-IA
-Score player
-Score IA
-Winner
-Looser
-start time
-end time


History of game
- List of all Games ID + tournaments ID

Leaderboard
- Player list sort by total score
- Player list sort by winner
- Player list sort by looser
"""
