from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment

def feed(request):
    """Выводит случайный список постов."""
    posts = Post.objects.all().order_by("?")
    return render(request, "feed/feed.html", {"posts": posts})

@login_required
@require_POST
def like_post(request, post_id):
    """Лайкает или убирает лайк с поста."""
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    post.update_like_count()
    return JsonResponse({"liked": liked, "like_count": post.like_count})

@login_required
@require_POST
def comment_post(request, post_id):
    """Добавляет комментарий к посту."""
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({"success": False, "message": "Комментарий не может быть пустым"})

    Comment.objects.create(user=request.user, post=post, content=content)
    return JsonResponse({"success": True, "message": "Комментарий добавлен"})
