from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats", related_query_name="participants", verbose_name="Участники")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено") 

    def get_chat_partner(self, current_user):
        if self.participants.count() == 2:
            return self.participants.exclude(id=current_user.id).first()
        return None  

    def __str__(self):
        return f"Чат #{self.id}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Чаты"
        verbose_name_plural = "Чаты"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", verbose_name="Чат")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Отправитель")
    text = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    read = models.BooleanField(default=False, verbose_name="Прочитано")
    updated = models.BooleanField(default=False, verbose_name="Отредактировано")

    def __str__(self):
        return f"Сообщение от {self.sender} в чате #{self.chat.id}: {self.text[:30]}..."

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщения"


class Call(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name='active_call', verbose_name="Чат")
    room_url = models.URLField(verbose_name="URL комнаты")
    created_at = models.DateTimeField(default=now, verbose_name="Создано")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
