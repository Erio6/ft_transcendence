import os.path
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField( default='avatar/default.jpg',upload_to='avatar')
    elo_rating = models.DecimalField(default=1500, max_digits=6, decimal_places=2)
    display_name = models.CharField(max_length=100, unique=True)
    is_online = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    country = CountryField(blank_label='(select country)',null=True,blank=True, default='LU')
    #wins = models.IntegerField(default=0)
    #losses = models.IntegerField(default=0)
    #total_points = models.IntegerField(default=0)
    #draws = models.IntegerField(default=0)
    #match_history = models.JSONField(default=list, blank=True)

    def update_elo(self, opponent_profile, is_winner, is_draw=False):
        k_factor = 32
        outcome = 0.5 if is_draw else (1.0 if is_winner else 0.0)
        expected_score = 1 / (1 + 10 ** ((opponent_profile.elo_rating - self.elo_rating) / 400))
        self.elo_rating += k_factor * (outcome - expected_score)
        self.save()
        if not is_draw:
            opponent_outcome = 0.5 if is_draw else (0.0 if is_winner else 1.0)
            opponent_expected_score = 1 / (1 + 10 ** ((self.elo_rating - opponent_profile.elo_rating) / 400))
            opponent_profile.elo_rating += k_factor * (opponent_outcome - opponent_expected_score)
            opponent_profile.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar and os.path.exists(self.avatar.path):
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    @property
    def leaderboard_rank(self):
        leaderboard = self.leaderboard
        return leaderboard.rank if leaderboard else None

    @property
    def total_wins(self):
        leaderboard = self.leaderboard  # Accessing the related leaderboard object
        return leaderboard.total_wins if leaderboard else 0  # Return 0 if no leaderboard exists

    @property
    def total_losses(self):
        leaderboard = self.leaderboard  # Accessing the related leaderboard object
        return leaderboard.total_losses if leaderboard else 0  # Return 0 if no leaderboard exists

    def __str__(self):
        return f'{self.user.username} Profile'
# Create your models here.
