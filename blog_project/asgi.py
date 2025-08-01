import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import blog.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# This is the main router for the application.
# It tells Channels how to handle different types of connections.
application = ProtocolTypeRouter({
    # For standard HTTP requests, use the default Django ASGI application.
    "http": get_asgi_application(),
    # For WebSocket connections, use our own routing configuration.
    "websocket": AuthMiddlewareStack(
        URLRouter(
            blog.routing.websocket_urlpatterns
        )
    ),
})
