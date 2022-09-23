from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('messages/', consumers.ChatConsumer.as_asgi()),
]