from django.urls import path
from .views import like_post, comment_post, feed

app_name = 'feed' 

urlpatterns = [
    path('', feed, name='feed'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('post/<int:post_id>/', comment_post, name='comment_post'),
]
