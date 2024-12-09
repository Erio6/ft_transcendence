from django.db import models
from django.utils import timezone
from user.models import UserProfile
from game.models import Game, SoloGame
from tournaments.models import TournamentGame
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from itertools import chain



# Create your models here.

class GameHistory(models.Model):
    game_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    game_id = models.PositiveIntegerField()
    game_object = GenericForeignKey('game_type', 'game_id')
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'GameHistory: {self.game_object}'


class Leaderboard(models.Model):
    player = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='leaderboard')
    total_points = models.IntegerField(default=0)
    total_wins = models.PositiveIntegerField(default=0)
    total_losses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Leaderboard: {self.player}'

    @staticmethod
    def update_leaderboard(): # TO USE ONLY IF THERE IS AN ISSUES IN REGISTERING THE SCORE, THIS FUNCTION WILL REBUILD THE LEADERBOARD ENTIRELY

        Leaderboard.objects.all().delete()

        multiplayer_games = list(chain(Game.objects.all(), TournamentGame.objects.all()))
        for game in multiplayer_games:
            # Update Player One
            Leaderboard.update_player_stats(
                player=game.player_one, points=game.player_one_score, win=(game.winner == game.player_one)
            )
            # Update Player Two
            Leaderboard.update_player_stats(
                player=game.player_two, points=game.player_two_score, win=(game.winner == game.player_two)
            )

        # Process all solo games
        solo_games = SoloGame.objects.all()
        for game in solo_games:
            # Update Solo Player
            Leaderboard.update_player_stats(
                player=game.player_solo, points=game.player_solo_score, win=(game.winner == game.player_solo)
            )

    @staticmethod
    def update_player_stats(player, points, win):
        # Get or create the leaderboard entry for the player
        leaderboard, created = Leaderboard.objects.get_or_create(player=player)

        # Update stats
        leaderboard.total_points += points
        if win:
            leaderboard.total_wins += 1
        else:
            leaderboard.total_losses += 1

        leaderboard.save()
