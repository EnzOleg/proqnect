from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('auth/', auth_view, name='auth'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profile/<int:user_id>/', profile_view, name='profile'),  
    path('profile/<int:user_id>/', profile_view, name='profile_detail'), 
    path('logout/', logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
    path("set-theme/", set_theme, name="set_theme"),
    path("add_post/", add_post, name="add_post"),
    path("edit_post/<int:post_id>/", edit_post, name="edit_post"),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path("delete_post/<int:post_id>/", delete_post, name="delete_post"),
]
