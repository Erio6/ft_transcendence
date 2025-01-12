from django.urls import path, include, re_path
from two_factor.urls import urlpatterns as tf_urls
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

import matchMaking
from game.consumers import GameConsumer
from matchMaking.consumers import MatchMakingConsumer
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from two_factor.views import SetupView

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('', include(tf_urls)),  # Admin route
    path('admin/', admin.site.urls),  # Admin route
    path('game/', include('game.urls')),
    path('auth/', include('authentication.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', include('user.urls')),
    path('friends/', include('friends.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('API.urls')),
    path('leaderboard/', include('dashboard.urls')),
    path('matchMaking', include('matchMaking.urls')),
    path('tournament/', include('tournaments.urls')),
]

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_id>\d+)/$', GameConsumer.as_asgi()), # Map WebSocket path to consumer
    re_path(r'ws/matchmaking/(?P<match_id>\d+)/$', MatchMakingConsumer.as_asgi()),
]

# only for production to change for deploying
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
