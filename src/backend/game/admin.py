from django.contrib import admin

# Register your models here.
from game.models import *
admin.site.register(Game)
admin.site.register(SoloGame)

