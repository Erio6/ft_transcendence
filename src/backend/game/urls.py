from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.quickPlay, name='play'),
    path('solo', views.soloGame, name='solo'),
    path('multi', views.game_creation, name='multi'),
    path('multi_scores/<int:game_id>', views.multi_scores, name='multi_scores'),
    # path('play/multi/game', views.test_pong_game, name='multi_game'),
]
