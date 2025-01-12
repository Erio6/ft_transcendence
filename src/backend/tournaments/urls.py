from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournaments_home, name='tournaments'),
    path('create', views.create_tournament, name='create_tournament'),
    path('join', views.join_tournament, name='join_tournament'),
]