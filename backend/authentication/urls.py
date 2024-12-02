from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('profile/<str:username>/edit/', views.edit_profile_view, name='edit_user_profile'),
]