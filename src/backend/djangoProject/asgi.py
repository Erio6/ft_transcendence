"""
ASGI config for djangoProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import asyncio
import os
import threading

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import matchMaking.routing
import game.routing
from game.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(game.routing.websocket_urlpatterns + matchMaking.routing.websocket_urlpatterns)
    ),
})

# threading.Thread(target=asyncio.run, args=(game_loop(),), daemon=True).start()
