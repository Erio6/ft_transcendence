from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from django.urls import path
from .views import protected_view
app_name = 'authentication'

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('protected/', protected_view, name='protected'),
]
