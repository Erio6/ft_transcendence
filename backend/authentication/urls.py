from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('friends/', views.friends_overview, name='friends'),
    path('friends/send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friends/accept/<int:friendship_id>/<str:action>/', views.respond_friend_request, name='respond_friend_request'),
    path('friends/remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('friends/cancel/<int:friendship_id>/', views.cancel_friend_request, name='cancel_friend_request'),
]