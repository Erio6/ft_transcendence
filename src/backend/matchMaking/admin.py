from django.contrib import admin
from .models import Match

# Register your models here.


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('player_one', 'player_two', 'status', 'created_at', 'connected_players_display')
    list_filter = ('status', 'created_at')
    search_fields = ('player_one__display_name', 'player_two__display_name')
    readonly_fields = ('connected_players_display',)

    def connected_players_display(self, obj):
        return ", ".join(obj.connected_players) if obj.connected_players else "No Players Connected"

    connected_players_display.short_description = "Connected Players"