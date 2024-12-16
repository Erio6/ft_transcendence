from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
]