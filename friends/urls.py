from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('add/<int:user_id>/', views.add_friend, name='add_friend'),
    path('accept/<int:request_id>/', views.accept_friend, name='accept_friend'),
    path('remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
]
