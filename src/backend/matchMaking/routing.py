from django.urls import re_path
from .consumers import MatchMakingConsumer


websocket_urlpatterns = [
    re_path(r'ws/matchmaking/(?P<match_id>\d+)/$', MatchMakingConsumer.as_asgi()),
]