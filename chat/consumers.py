import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connection established. Room group: {self.roomGroupName}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )
        print(f"WebSocket connection closed. Room group: {self.roomGroupName}")

    async def receive(self, text_data):
        print(f"Received data: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        recipient = text_data_json["recipient"]
        await self.save_message(username, recipient, message)  # Save the message in the database
        await self.channel_layer.group_send(
            self.roomGroupName,
            {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "recipient": recipient,
            }
        )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        recipient = event["recipient"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "recipient": recipient}))
        print(f"Message sent: {message} - Username: {username} - Recipient: {recipient}")

    @sync_to_async
    def save_message(self, sender_username, recipient_username, message):
        from .models import ChatRoom, ChatMessage

        # Concatenate the sender's username and recipient's username
        chatroom_name = f"{sender_username}_{recipient_username}"
        # Check if the chat room already exists or create a new one
        try:
            room = ChatRoom.objects.get(name=chatroom_name)
        except ChatRoom.DoesNotExist:
            room = ChatRoom.objects.create(name=chatroom_name)
        sender = self.get_user(sender_username)
        recipient = self.get_user(recipient_username)
        chat_message = ChatMessage(room=room, sender=sender, recipient=recipient, message=message)
        print(chat_message)
        chat_message.save()

    def get_user(self, username):
        from django.contrib.auth.models import User
        return User.objects.get(username=username)
