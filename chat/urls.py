from django.urls import path
from . import api


urlpatterns = [
    path('api/v1/fetch-chat-messages/<str:sender_username>/<str:recipient_username>/', api.fetch_chat_messages, name='fetch_chat_messages'),
    path('api/v1/delete-chat-message/<int:message_id>/', api.delete_chat_message, name='delete_chat_message'),
	
]
