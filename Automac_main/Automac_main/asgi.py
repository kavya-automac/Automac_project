from channels.auth import AuthMiddlewareStack

print("ASGIIII")

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
# from ..app import routing
from Automac_app import routing
# from * import app
# from ..app import *




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro.settings')
# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(URLRouter(
        routing.websocket_urlpatterns
    ))
})


