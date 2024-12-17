from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    # path('gameHistory/', views.game_history_view, name='gameHistory'),
]