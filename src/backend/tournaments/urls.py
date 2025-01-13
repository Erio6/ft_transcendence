from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournaments_home, name='tournaments'),
    path('create', views.create_tournament, name='create_tournament'),
    path('join', views.join_tournament, name='join_tournament'),
    path('waiting-room/<int:tournament_id>/', views.tournament_waiting_room, name='waiting_room'),
    path('cancel', views.cancel_tournament, name='cancel_tournament'),
]