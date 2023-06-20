from django.db import models
from accounts.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    deletedBySender = models.BooleanField(default=False)
    deletedByRecipient = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.name}"
