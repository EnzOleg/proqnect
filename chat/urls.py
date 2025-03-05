from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('<int:chat_id>/', views.chat_room, name='chat_room'),
    path('with/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('consultation/<int:user_id>/', views.consultation_chat_with_expert, name='consultation_chat_with_expert'),
]
