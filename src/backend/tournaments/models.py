from django.contrib.auth.models import User
from django.db import models
from user.models import UserProfile
from game.models import Game

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    created_by = models.ForeignKey(UserProfile, related_name='tournament_creator' ,on_delete=models.CASCADE)
    tournament_code_join = models.CharField(max_length=4, unique=True)
    players = models.ManyToManyField(UserProfile, through='TournamentPlayer')
    status = models.CharField(
        max_length=20,
        choices=[('waiting', 'Waiting for players'), ('ongoing', 'Ongoing'), ('completed', 'Completed')],
        default='waiting'
    )
    def __str__(self):
        return self.name

class TournamentPlayer(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_eliminated = models.BooleanField(default=False)
    round_reached = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.player.display_name} in {self.tournament.name}"

class TournamentGame(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player_one = models.ForeignKey(TournamentPlayer, related_name='tournament_player_one' ,on_delete=models.CASCADE, null=True, blank=True)
    player_two = models.ForeignKey(TournamentPlayer, related_name='tournament_player_two',on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    winner = models.ForeignKey(TournamentPlayer, related_name='game_winner', null=True, on_delete=models.SET_NULL)
    round_number = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_games')

    
