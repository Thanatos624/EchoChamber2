import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    """
    A consumer to handle WebSocket chat connections for a specific blog post.
    """
    async def connect(self):
        """
        Called when the websocket is handshaking as part of the connection.
        """
        # Get the post ID from the URL. The URL will look like /ws/chat/123/
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'chat_{self.post_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive a message from the WebSocket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        """
        Receive message from room group and send it to the WebSocket.
        """
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
