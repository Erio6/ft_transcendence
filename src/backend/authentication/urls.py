from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.register, name='register'),
]