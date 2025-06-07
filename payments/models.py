from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[
        ("pending", "Ожидание"),
        ("paid", "Оплачено"),
        ("failed", "Неудача"),
        ("canceled", "Отменено")
    ], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Платеж пользователя {self.user.email} на сумму {self.amount} от {self.created_at:%d.%m.%Y %H:%M} со статусом {self.status}"


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Баланс пользователься {self.user.email} составляет {self.balance}"