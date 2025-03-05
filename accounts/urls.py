from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', auth_view, name='auth'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/update_status/', update_status, name='update_status'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
    path("add_post/", add_post, name="add_post"),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path("set-theme/", set_theme, name="set_theme"),
]
