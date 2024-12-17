from django.urls import path
from . import views

app_name = 'API'

urlpatterns = [
    path('score', views.game_update, name='game_update'),
    path('scorehistory', views.GameHistoryView.as_view(), name='score_history_api'),
]