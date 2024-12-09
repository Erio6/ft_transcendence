from django.contrib import admin

# Register your models here.
from tournaments.models import Tournament
from tournaments.models import TournamentPlayer
from tournaments.models import TournamentGame
admin.site.register(Tournament)
admin.site.register(TournamentPlayer)
admin.site.register(TournamentGame)