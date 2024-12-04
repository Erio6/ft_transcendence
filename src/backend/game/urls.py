from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('play/' , views.quickPlay, name='play'),
    path('play/solo', views.soloGame, name='solo'),
    path('play/multi', views.multiGame, name='multi'),
    path('play/multi/game', views.test_pong_game, name='multi_game'),
]