from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('<str:username>/edit/', views.edit_profile_view, name='edit_profile'),
    path('edit/pwd/', views.change_password, name='change_password'),
]