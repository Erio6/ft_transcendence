from django.contrib.auth.models import User
from django.db import models
from user.models import *

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(UserProfile, through='TournamentPlayer')
    def __str__(self):
        return self.name

class TournamentPlayer(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)
    def __str__(self):
        return self.tournament.name