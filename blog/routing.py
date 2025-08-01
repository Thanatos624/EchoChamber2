from django.urls import re_path
from . import consumers

# This is like urls.py, but for WebSocket connections.
websocket_urlpatterns = [
    # This regex matches URLs like /ws/chat/123/ and captures the post ID.
    re_path(r'ws/chat/(?P<post_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
