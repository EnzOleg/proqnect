import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Chat, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"
        
        self.chat = await sync_to_async(Chat.objects.filter(id=self.chat_id).first, thread_sensitive=True)()
        if not self.chat:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send_chat_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get("message", "").strip()

        user = self.scope["user"]
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({"error": "Вы не авторизованы"}))
            return

        if not message_text:
            await self.send(text_data=json.dumps({"error": "Сообщение не может быть пустым"}))
            return

        message = await self.save_message(user, message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message.text,
                "sender": user.get_full_name() or user.email,
                "sender_id": user.id,  # Добавлено поле sender_id
                "avatar": user.profile_picture.url if hasattr(user, 'profile_picture') and user.profile_picture else "/static/avatars/def_icon.png",
                "profile_url": user.profile_url if hasattr(user, 'profile_url') else "#",
                "timestamp": message.timestamp.isoformat()
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "sender_id": event["sender_id"],  # Передаём sender_id клиенту
            "avatar": event["avatar"],
            "profile_url": event["profile_url"],
            "timestamp": event["timestamp"]
        }))

    async def send_chat_history(self):
        history = await self.get_chat_history()
        await self.send(text_data=json.dumps({"history": history}))

    @sync_to_async
    def get_chat_history(self):
        if not self.chat:
            return []
        
        messages = Message.objects.filter(chat=self.chat).order_by("timestamp")
        return [
            {
                "message": msg.text,
                "sender": msg.sender.get_full_name() or msg.sender.email,
                "sender_id": msg.sender.id,  # Добавлено поле sender_id
                "avatar": msg.sender.profile_picture.url if hasattr(msg.sender, 'profile_picture') and msg.sender.profile_picture else "/static/avatars/def_icon.png",
                "profile_url": msg.sender.profile_url if hasattr(msg.sender, 'profile_url') else "#",
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]

    @sync_to_async
    def save_message(self, user, text):
        return Message.objects.create(chat=self.chat, sender=user, text=text)
