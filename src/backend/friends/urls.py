from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.friends_overview, name='friends_overview'),
    path('send_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('cancel_request/<int:request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
]