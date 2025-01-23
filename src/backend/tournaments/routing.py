from django.urls import re_path
from tournaments.consumers import TournamentConsumer

websocket_urlpatterns = [
    re_path(r'ws/tournaments/(?P<tournament_id>\d+)/$', TournamentConsumer.as_asgi()),
]