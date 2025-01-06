from django.urls import path
from .consumers import MatchMakingConsumer


websocket_urlpatterns = [
    path('ws/matchmaking/', MatchMakingConsumer.as_asgi()),
]