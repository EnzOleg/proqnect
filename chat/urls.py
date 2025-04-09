from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('<int:chat_id>/', views.chat_room, name='chat_room'),
    path('with/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path("create-or-get-call/<int:chat_id>/", views.create_or_get_call, name="create_or_get_call"),
    path("check-call/<int:chat_id>/", views.check_active_call, name="check_active_call"),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]
