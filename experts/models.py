from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
User = get_user_model()

User = get_user_model()

class Expert(models.Model):
    SPECIALIZATIONS = [
    ("developer", "Разработчик"),
    ("designer", "Дизайнер"),
    ("marketing", "Маркетинг"),
    ("finance", "Финансы"),
    ("cybersport", "Киберспорт"),
    ("analyst", "Аналитик"),
    ("manager", "Менеджер"),
    ("programmer", "Программист"),
    ("architect", "Архитектор"),
    ("copywriter", "Копирайтер"),
    ("psychologist", "Психолог"),
    ("journalist", "Журналист"),
    ("translator", "Переводчик"),
    ("teacher", "Педагог"),
    ("photographer", "Фотограф"),
    ("web_developer", "Веб-разработчик"),
    ("mobile_developer", "Мобильный разработчик"),
    ("sys_admin", "Системный администратор"),
    ("tester", "Тестировщик"),
    ("db_admin", "Администратор базы данных"),
    ("network_engineer", "Сетевой инженер"),
    ("seo_specialist", "SEO-специалист"),
    ("ui_ux_designer", "UI/UX дизайнер"),
    ("devops_engineer", "DevOps-инженер"),
    ("strategy_consultant", "Стратегический консультант"),
    ("lawyer", "Юрист"),
    ("doctor", "Врач"),
    ("coach", "Тренер"),
    ("personal_trainer", "Персональный тренер"),
    ("financial_advisor", "Финансовый консультант"),
    ("pr_manager", "PR-менеджер"),
    ("social_worker", "Социальный работник"),
    ("sales_specialist", "Специалист по продажам"),
    ("content_manager", "Контент-менеджер"),
    ("recruiter", "Рекрутер"),
    ("other", "Другое"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="expert_profile")
    specialization = models.CharField(max_length=255, verbose_name="Специализация", choices=SPECIALIZATIONS,blank=True)
    custom_specialization = models.CharField(max_length=255, verbose_name="Своя специализация", blank=True)
    bio = models.TextField(verbose_name="О себе", blank=True)
    experience = models.IntegerField(verbose_name="Опыт (лет)", default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    price_per_hour = models.DecimalField(verbose_name="Цена за час", max_digits=10, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False, verbose_name="Верифицирован")

    def get_specialization_display(self):
        if self.specialization == "other" and self.custom_specialization:
            return self.custom_specialization
        return dict(self.SPECIALIZATIONS).get(self.specialization, "Не указано")
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            return total_rating / len(reviews)
        return None 

    def __str__(self):
        return f"Эксперт {self.user.email}"
    
    class Meta:
        verbose_name = "Эксперты"
        verbose_name_plural = "Эксперты"

class ExpertSkill(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100, verbose_name="Навык")

    def __str__(self):
        return f"{self.expert.user.first_name} {self.expert.user.last_name}: {self.expert.user.email}"
    
    class Meta:
        verbose_name = "Навыки"
        verbose_name_plural = "Навыки"

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "expert" )
        verbose_name = "Отзывы"
        verbose_name_plural = "Отзывы"

