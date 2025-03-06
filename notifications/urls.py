from django.urls import path
from .views import get_notifications, mark_as_read

urlpatterns = [
    path("get/", get_notifications, name="get_notifications"),
    path("read/", mark_as_read, name="mark_notifications_as_read"),

]
