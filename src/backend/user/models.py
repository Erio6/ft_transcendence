import os.path
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField( default='avatar/default.jpg',upload_to='avatar')
    display_name = models.CharField(max_length=100, unique=True)
    # wins = models.IntegerField(default=0)
    # losses = models.IntegerField(default=0)
    # total_points = models.IntegerField(default=0)
    # draws = models.IntegerField(default=0)
    # match_history = models.JSONField(default=list, blank=True)

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
