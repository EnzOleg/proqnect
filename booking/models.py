from django.db import models
from django.utils.timezone import now
from accounts.models import CustomUser

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено'),
        ('completed', 'Выполнено'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings', verbose_name="Клиент")
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments', verbose_name="Эксперт")
    scheduled_time = models.DateTimeField(verbose_name="Дата и время консультации", null=True, blank=True)
    room_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    
    problem_description = models.TextField(verbose_name="Описание проблемы", blank=True, null=True)
    available_times = models.TextField(verbose_name="Предпочтительные временные интервалы", blank=True, null=True,
                                       help_text="Укажите удобное для вас время. Можно перечислить несколько вариантов, разделив запятыми.")
    
    def __str__(self):
        return f"Бронь {self.user.email} у {self.expert.email} ({self.get_status_display()})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Записи"
        verbose_name_plural = "Записи"
