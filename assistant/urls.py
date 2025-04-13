from django.urls import path
from .views import gpt_assist, gpt_chat_assistent


app_name = 'assistant'

urlpatterns = [
    path('api/', gpt_assist, name="ask_gpt"),
    path('chat-api/', gpt_chat_assistent, name="chat-assistant")
]
