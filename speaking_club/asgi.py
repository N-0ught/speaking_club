"""
ASGI config for speaking_club project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speaking_club.settings')
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()
# django.setup()
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import club.routing

application = ProtocolTypeRouter({
    "https": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                club.routing.websocket_urlpatterns
            )
        )
    ),
})