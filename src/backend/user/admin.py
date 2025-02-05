from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'is_online', 'is_banned', 'country', 'avatar_display')
    list_filter = ('is_online', 'is_banned', 'country')
    search_fields = ('user__username', 'display_name', 'country')
    readonly_fields = ('avatar_display',)

    def avatar_display(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="50" height="50" style="border-radius: 50%;" />'
        return "No Image"

    avatar_display.allow_tags = True
    avatar_display.short_description = "Avatar Preview"