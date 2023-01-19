"""
ASGI config for jobya project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# import os
# from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter

# import chat.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobya.settings')


# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     )
# })

# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobya.settings')
# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     # Just HTTP for now. (We can add other protocols later.)
# })

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobya.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter( chat.routing.websocket_urlpatterns)
        )
    ),
})
