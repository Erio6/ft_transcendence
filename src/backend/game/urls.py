from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.welcome, name='welcome'),
]