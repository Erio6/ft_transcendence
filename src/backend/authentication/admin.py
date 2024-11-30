from django.contrib import admin

# Register your models here.
from authentication.models import PlayerProfile

class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'friends_number', 'total_points', 'wins', 'losses', 'draws')
admin.site.register(PlayerProfile, PlayerProfileAdmin)
