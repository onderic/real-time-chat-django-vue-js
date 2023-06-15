from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
from . import api


urlpatterns = [
	# path("", chat_views.chatPage, name="chat-page"),
    path('api/v1/fetch-chat-messages/<str:sender_username>/<str:recipient_username>/', api.fetch_chat_messages, name='fetch_chat_messages'),
	
]
