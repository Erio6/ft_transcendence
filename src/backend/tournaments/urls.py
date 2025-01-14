from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournaments_home, name='tournaments'),
    path('create', views.create_tournament, name='create_tournament'),
    path('join', views.join_tournament, name='join_tournament'),
    path('waiting-room/<int:tournament_id>/', views.tournament_waiting_room, name='waiting_room'),
    path('cancel/<int:tournament_id>/', views.cancel_tournament, name='cancel_tournament'),
    path('leave/<int:tournament_id>/', views.leave_tournament, name='leave_tournament'),
    path('start/<int:tournament_id>/', views.start_tournament, name='start_tournament'),
    path('tree/<int:tournament_id>/', views.tournament_tree_view, name='tournament_tree'),
]