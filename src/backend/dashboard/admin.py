# admin.py
from django.contrib import admin
from .models import Leaderboard


class LeaderboardAdmin(admin.ModelAdmin):
    # Display these fields in the list view.
    list_display = ('player', 'elo', 'total_wins', 'total_losses', 'rank')

    # Add filters to the sidebar (you can add more fields as needed).
    list_filter = ('rank',)

    # Enable search by player's username.
    search_fields = ('player__username',)

    # Order leaderboards by elo descending by default.
    ordering = ('-elo',)

    # Optionally, if you want to show all fields in the detail view,
    # you can set the fields explicitly (or remove this to use the default form).
    fields = ('player', 'elo', 'total_wins', 'total_losses', 'rank')


# Register the Leaderboard model with its admin configuration.
admin.site.register(Leaderboard, LeaderboardAdmin)


