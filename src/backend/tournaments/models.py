from django.contrib.auth.models import User
from django.db import models
from user.models import UserProfile

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    created_by = models.ForeignKey(UserProfile, related_name='tournament_creator' ,on_delete=models.CASCADE)
    players = models.ManyToManyField("self", through='TournamentPlayer')
    def __str__(self):
        return self.name

class TournamentPlayer(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    winner = models.ForeignKey(UserProfile, related_name='tournament_winner',on_delete=models.CASCADE)
    def __str__(self):
        return self.tournament.name

class TournamentGame(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player_one = models.ForeignKey(UserProfile, related_name='tournament_player_one' ,on_delete=models.CASCADE)
    player_two = models.ForeignKey(UserProfile, related_name='tournament_player_two',on_delete=models.CASCADE)
    winner = models.ForeignKey(UserProfile, related_name='tournament_game_winner',on_delete=models.CASCADE)
    looser = models.ForeignKey(UserProfile, related_name='tournament_game_looser',on_delete=models.CASCADE)
    player_one_score = models.IntegerField(default=0)
    player_two_score = models.IntegerField(default=0)
    winner_score = models.IntegerField(default=0)
    looser_score = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return  f'{self.player_one.display_name} vs {self.player_two.display_name} (Tournament)'

    # - Tournament game (player one, player two, game ID, tournament ID)
    # - Tournament (je reprend le model tournament qui existe deja)
    # - Je rajoute un bool dans game pour savoir si la game est tournament ou non
    # - Dans leaderboard j'affiche que les game ou le tournament bool est false
    
