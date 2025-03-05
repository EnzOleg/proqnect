from django.db import models
from django.contrib.auth import get_user_model
from booking.models import Booking

User = get_user_model()

class Chat(models.Model):
    CHAT_TYPE_CHOICES = [
        ('consultation', 'Консультация'),
        ('social', 'Социальный'),
    ]
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPE_CHOICES, default='social', verbose_name="Тип чата")
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True, related_name='chat', verbose_name="Бронирование")
    participants = models.ManyToManyField(User, related_name="chats", related_query_name="participants")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено") 

    def get_chat_partner(self, current_user):
        """ Возвращает собеседника, если чат приватный """
        if self.participants.count() == 2:
            return self.participants.exclude(id=current_user.id).first()
        return None  # В групповом чате нет единственного собеседника

    def __str__(self):
        if self.chat_type == "consultation" and self.booking:
            return f"Консультация (Booking #{self.booking.id})"
        return f"Социальный чат #{self.id}"

    class Meta:
        ordering = ['-updated_at']  # Последние обновленные чаты в начале


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", verbose_name="Чат")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Отправитель")
    text = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    read = models.BooleanField(default=False, verbose_name="Прочитано")

    def __str__(self):
        return f"Сообщение от {self.sender} в чате #{self.chat.id}: {self.text[:30]}..."
    
    class Meta:
        ordering = ['timestamp']
