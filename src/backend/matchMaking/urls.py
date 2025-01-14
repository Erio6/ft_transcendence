from django.urls import path
from . import views

app_name = 'matchMaking'

urlpatterns = [
    path('matchmaking', views.waiting_view, name='matchmaking'),
]