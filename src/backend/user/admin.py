from django.contrib import admin
from .models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'display_name', 'total_points', 'wins', 'losses', 'draws')
admin.site.register(UserProfile, UserProfileAdmin)