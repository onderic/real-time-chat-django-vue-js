from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import ChatMessage



@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_chat_messages(request, sender_username, recipient_username):
    chat_messages = ChatMessage.objects.filter(
        sender__username=sender_username,
        recipient__username=recipient_username
    ).order_by('timestamp')

    # Serialize the chat messages
    serialized_messages = []
    for message in chat_messages:
        serialized_message = {
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'message': message.message,
            'timestamp': message.timestamp
        }
        serialized_messages.append(serialized_message)

    # print('Serialized Messages:', serialized_messages) 

    return Response(serialized_messages)

