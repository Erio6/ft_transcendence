from django.contrib.auth.models import User
from django.db import models
from user.models import UserProfile
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Game(models.Model):
    game_histories = GenericRelation('dashboard.GameHistory',
                                     content_type_field='game_type',
                                     object_id_field='game_id')
    player_one = models.ForeignKey(UserProfile, related_name='player_one_games', on_delete=models.CASCADE)
    player_two = models.ForeignKey(UserProfile, related_name='player_two_games', null=True, blank=True, on_delete=models.CASCADE)
    winner = models.ForeignKey(UserProfile, related_name='winner_games', null=True, on_delete=models.SET_NULL)
    looser = models.ForeignKey(UserProfile, related_name='looser_games', null=True, on_delete=models.SET_NULL)
    player_one_score = models.IntegerField(default=0, null=True, blank=True)
    player_two_score = models.IntegerField(default=0, null=True, blank=True)
    winner_score = models.IntegerField(default=0, null=True, blank=True)
    looser_score = models.IntegerField(default=0, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    tx_hash = models.CharField(max_length=66, blank=True, null=True)
    is_recorded_on_blockchain = models.BooleanField(default=False)
    type_of_game = models.CharField(max_length=20, choices=[('multiplayer', 'Multiplayer'), ('solo_IA_easy', 'Solo IA Easy'), ('solo_IA_medium', 'Solo IA Medium'), ('solo_IA_hard', 'Solo IA Hard'), ('solo_player', 'Solo Player'), ('tournament', 'Tournament')], default='multiplayer')

    def __str__(self):
        if self.player_two:
            return f'{self.player_one.display_name} vs {self.player_two.display_name}'
        else:
            return f'{self.player_one.display_name} is waiting an opponent in {self.id}'

    @property
    def tx_url(self):
        if self.tx_hash:
            if self.tx_hash.startswith('0x'):
                return f"https://sepolia.etherscan.io/tx/{self.tx_hash}"
            else:
                return f"https://sepolia.etherscan.io/tx/0x{self.tx_hash}"
        return None


class SoloGame(models.Model):
    player_solo = models.ForeignKey(UserProfile, related_name='player_one_games_solo', on_delete=models.CASCADE)
    winner = models.ForeignKey(UserProfile, related_name='winner_games_solo', null=True, on_delete=models.CASCADE)
    looser = models.ForeignKey(UserProfile, related_name='looser_games_solo', null=True, on_delete=models.CASCADE)
    player_solo_score = models.IntegerField(default=0)
    IA_score = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
