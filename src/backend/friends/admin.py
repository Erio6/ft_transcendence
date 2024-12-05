from django.contrib import admin
from .models import FriendList, FriendRequest

# Register your models
class FriendListAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'friends_count']
    readonly_fields = ['friends']

    def friends_count(self, obj):
        return obj.friends.count()
    friends_count.short_description = 'Number of Friends'

    class Meta:
        model = FriendList
admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['sender__user__username', 'receiver__user__username']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)


from django.contrib import admin

# Register your models here.
