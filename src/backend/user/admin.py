from django.contrib import admin
from .models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'display_name', 'is_online')
admin.site.register(UserProfile, UserProfileAdmin)