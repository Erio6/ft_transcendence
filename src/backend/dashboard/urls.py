from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('gameHistory/', views.game_history_view, name='gameHistory'),
]