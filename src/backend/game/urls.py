from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.quickPlay, name='play'),
    path('solo', views.soloGame, name='solo'),
    #path('multi', views.game_creation, name='multi'),
    # path('multi', views.multiGame, name='multi'),
    # path('multi_scores/<int:game_id>', views.multi_scores, name='multi_scores'),
    # path('play/multi/game', views.test_pong_game, name='multi_game'),
    path('online', views.online_game_creation, name='online'),
    path('game/<int:game_id>', views.game_3d, name='real_game'),
    path('end/<int:game_id>/', views.end_game, name='game_end'),
]
