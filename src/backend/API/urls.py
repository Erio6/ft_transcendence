from django.urls import path
from . import views

app_name = 'API'

urlpatterns = [
    path('score', views.ScoreView.as_view(), name='score_api'),
    path('scorehistory', views.GameHistoryView.as_view(), name='score_history_api'),
]