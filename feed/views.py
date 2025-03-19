from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment

@login_required
def feed(request):
    posts = Post.objects.all().order_by("?")
    
    liked_posts = set()
    if request.user.is_authenticated:
        liked_posts = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
    
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()
        post.top_comments = post.comments.filter(parent__isnull=True).order_by("created_at")
        
        for top_comment in post.top_comments:
            branch = [comment for comment in post.comments.all() if comment.parent and comment.top_parent.id == top_comment.id]
            branch.sort(key=lambda x: x.created_at)
            top_comment.branch_replies = branch
    
    return render(request, "feed/feed.html", {"posts": posts, "liked_posts": liked_posts})



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
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()
    parent_id = request.POST.get("parent_id")
    
    if not content:
        return JsonResponse({"success": False, "message": "Комментарий не может быть пустым"})
    
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)
        # Если parent уже имеет родителя, используем верхнего родителя
        if parent.parent:
            effective_parent = parent.top_parent
        else:
            effective_parent = parent
        comment = Comment.objects.create(user=request.user, post=post, content=content, parent=effective_parent)
        parent_author = f"{effective_parent.user.first_name} {effective_parent.user.last_name}"
        effective_parent_id = effective_parent.id
    else:
        comment = Comment.objects.create(user=request.user, post=post, content=content)
        parent_author = ""
        effective_parent_id = comment.id  # для топ-комментария, он сам является эффективным родителем
    
    return JsonResponse({
        "success": True,
        "message": "Комментарий добавлен",
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "avatar_url": request.user.profile_picture.url if request.user.profile_picture else "",
        "created_at": comment.created_at.strftime("%d %b %Y %H:%M"),
        "comment_id": comment.id,
        "parent_author": parent_author,
        "effective_parent_id": effective_parent_id,
    })


