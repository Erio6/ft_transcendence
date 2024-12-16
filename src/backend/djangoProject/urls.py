from django.urls import path, include, re_path
from two_factor.urls import urlpatterns as tf_urls
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from game.consumers import GameConsumer
from . import views

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
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('', include(tf_urls)),  # Admin route
    path('admin/', admin.site.urls),  # Admin route
    path('game/', include('game.urls')),
    path('auth/', include('authentication.urls')),
    path('user/', include('user.urls')),
    path('friends/', include('friends.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('API.urls')),
    path('leaderboard/', include('dashboard.urls')),
]

websocket_urlpatterns = [
    re_path(r'ws/game/$', GameConsumer.as_asgi()),  # Map WebSocket path to consumer
]

# only for production to change for deploying
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
