from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def get_notifications(request):
    """Возвращает список непрочитанных уведомлений"""
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).values("id", "description", "link")
    return JsonResponse(list(notifications), safe=False)


@login_required
def mark_as_read(request):
    """Отмечает все уведомления как прочитанные"""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"status": "ok"})
