from django.contrib import admin
from .models import UserProfile, FriendList, FriendRequest

# Register your models here.
admin.site.register(UserProfile)

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user_profile__user__username']
    list_display = ['user_profile']
    search_fields = ['user_profile__user__username']
    readonly_fields = ['user_profile']

    class Meta:
        model = FriendList
admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender__user__username', 'receiver__user__username']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__user__username', 'receiver__user__username']

    class Meta:
        model =FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)


