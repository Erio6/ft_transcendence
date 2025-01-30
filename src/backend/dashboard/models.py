from django.db import models
from django.utils import timezone
from user.models import UserProfile
from game.models import Game, SoloGame
from tournaments.models import TournamentGame
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from itertools import chain
from dashboard.signals import update_ranks
from decimal import Decimal



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
    elo = models.IntegerField(default=1500)
    total_wins = models.PositiveIntegerField(default=0)
    total_losses = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    def update_elo(self, opponent_leaderboard, is_winner, is_draw=False):
        k_factor = 32
        outcome = 1.0 if is_winner else 0.0
        expected_score = 1 / (1 + 10 ** ((opponent_leaderboard.elo - self.elo) / 400))
        new_elo = self.elo + k_factor * (outcome - expected_score)
        self.elo = int(round(new_elo))
        opponent_outcome = 1.0 - outcome  # if self won, opponent gets 0; else 1
        opponent_expected_score = 1.0 / (1.0 + 10.0 ** ((self.elo - opponent_leaderboard.elo) / 400.0))
        new_opponent_elo = opponent_leaderboard.elo + k_factor * (opponent_outcome - opponent_expected_score)
        opponent_leaderboard.elo = int(round(new_opponent_elo))
        self.save()
        opponent_leaderboard.save()

    def update_player_stats(self, opponent_leaderboard, is_winner):
        if is_winner:
            self.total_wins += 1
        else:
            self.total_losses += 1

        opponent_leaderboard.save()
        update_ranks()

    def __str__(self):
        return f'Leaderboard: {self.player}'

    # @staticmethod
    # def update_leaderboard(): # TO USE ONLY IF THERE IS AN ISSUES IN REGISTERING THE SCORE, THIS FUNCTION WILL REBUILD THE LEADERBOARD ENTIRELY
    #
    #     Leaderboard.objects.all().delete()
    #
    #     multiplayer_games = list(chain(Game.objects.all(), TournamentGame.objects.all()))
    #     for game in multiplayer_games:
    #         # Update Player One
    #         Leaderboard.update_player_stats(
    #             player=game.player_one, points=game.player_one_score, win=(game.winner == game.player_one)
    #         )
    #         # Update Player Two
    #         Leaderboard.update_player_stats(
    #             player=game.player_two, points=game.player_two_score, win=(game.winner == game.player_two)
    #         )
    #
    #     # Process all solo games
    #     solo_games = SoloGame.objects.all()
    #     for game in solo_games:
    #         # Update Solo Player
    #         Leaderboard.update_player_stats(
    #             player=game.player_solo, points=game.player_solo_score, win=(game.winner == game.player_solo)
    #         )
