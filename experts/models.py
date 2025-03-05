from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Expert(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="expert_profile")
    specialization = models.CharField(max_length=255, verbose_name="Специализация", blank=True)
    bio = models.TextField(verbose_name="О себе", blank=True)
    experience = models.IntegerField(verbose_name="Опыт (лет)", default=0)
    price_per_hour = models.DecimalField(verbose_name="Цена за час", max_digits=10, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False, verbose_name="Верифицирован")

    def __str__(self):
        return f"Эксперт {self.user.email}"

class ExpertSkill(models.Model):

    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100, verbose_name="Навык")

    def __str__(self):
        return f"{self.expert.user.username}: {self.name}"

class ExpertReview(models.Model):

    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    rating = models.IntegerField(verbose_name="Оценка", choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField(verbose_name="Отзыв", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f"Отзыв {self.user.username} -> {self.expert.user.username}"
