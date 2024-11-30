from django.contrib import admin
from .models import UserProfile, Friendship

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Friendship)
