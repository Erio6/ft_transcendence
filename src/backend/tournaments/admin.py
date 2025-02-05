from django.contrib import admin

# Register your models here.
from tournaments.models import Tournament
from tournaments.models import TournamentPlayer
from tournaments.models import TournamentGame

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_by', 'tournament_code_join', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'tournament_code_join', 'created_by__display_name')
    ordering = ('-start_date',)

@admin.register(TournamentPlayer)
class TournamentPlayerAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player', 'is_eliminated', 'round_reached')
    list_filter = ('is_eliminated', 'round_reached')
    search_fields = ('tournament__name', 'player__display_name')

@admin.register(TournamentGame)
class TournamentGameAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player_one', 'player_two', 'game', 'winner', 'round_number', 'parent')
    list_filter = ('round_number',)
    search_fields = ('tournament__name', 'player_one__player__display_name', 'player_two__player__display_name', 'winner__player__display_name')