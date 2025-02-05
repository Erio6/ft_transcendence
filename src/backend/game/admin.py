from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Game
from dashboard.models import GameHistory

class GameHistoryInline(GenericTabularInline):
    model = GameHistory
    # Specify the fields that link the generic relation.
    ct_field = "game_type"  # This should match the 'content_type_field' in your GenericRelation.
    ct_fk_field = "game_id"  # This should match the 'object_id_field' in your GenericRelation.
    extra = 0  # Number of extra blank inlines to show.


class GameAdmin(admin.ModelAdmin):
    # Customize the fields displayed in the list view.
    list_display = (
        'id',
        'player_one',
        'player_two',
        'winner',
        'looser',
        'player_one_score',
        'player_two_score',
        'winner_score',
        'looser_score',
        'start_time',
        'end_time',
        'is_completed',
        'tx_hash',
        'is_recorded_on_blockchain',
        'type_of_game',
    )

    # Add filters for easier navigation.
    list_filter = ('is_completed', 'is_recorded_on_blockchain', 'type_of_game')

    # Enable search by tx_hash and related user fields (adjust field names if needed).
    search_fields = (
        'tx_hash',
        'player_one__username',
        'player_two__username',
        'winner__username',
        'looser__username',
    )

    # Include the inline for GameHistory objects.
    inlines = [GameHistoryInline]

    # Make certain fields read-only.
    readonly_fields = ('start_time',)


# Register the Game model with its admin configuration.
admin.site.register(Game, GameAdmin)
