from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserRegistrationForm, PostEditForm
from .models import CustomUser, Post
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from friends.models import Friendship

def auth_view(request):
    form = CustomUserRegistrationForm()
    return render(request, "accounts/auth.html", {"form": form})

def register_view(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(request, "Регистрация успешна! Добро пожаловать!")
            return redirect("index")

        for field, errors in form.errors.items():
            field_obj = form.fields.get(field)
            field_label = field_obj.label if field_obj and field_obj.label is not None else ""
            for error in errors:
                messages.error(request, f"{field_label}: {error}" if field_label else error)

        return render(request, "accounts/auth.html", {"form": form, "show_register": True})

    return redirect("accounts:auth")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")

        messages.error(request, "Неправильный email или пароль")
        return render(request, "accounts/auth.html", {"show_login": True})

    return redirect("accounts:auth")

@login_required
def settings_view(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)

        status = request.POST.get("status")
        if status is not None:
            user.status = status

        user.timezone = request.POST.get("timezone", user.timezone)
        user.bio = request.POST.get("bio", user.bio)
        if request.FILES.get("profile_picture"):
            user.profile_picture = request.FILES["profile_picture"]
        if request.FILES.get("cover_photo"):
            user.cover_photo = request.FILES["cover_photo"]    
        user.save()
        messages.success(request, "Настройки обновлены!")
        return redirect("accounts:settings")

    return render(request, "accounts/settings.html", {"user": request.user})

def logout_view(request):
    logout(request)
    return redirect("accounts:auth")

@login_required
def profile_view(request, user_id=None):
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user 

    posts = user.posts.all().order_by("-created_at")
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()
        post.top_comments = post.comments.filter(parent__isnull=True).order_by("created_at")

        for top_comment in post.top_comments:
            branch = [comment for comment in post.comments.all() if comment.parent and comment.top_parent.id == top_comment.id]
            branch.sort(key=lambda x: x.created_at)
            top_comment.branch_replies = branch

    friends = Friendship.objects.filter(user=user).values_list("friend", flat=True)
    is_friend = request.user.id in friends

    return render(request, "accounts/profile.html", {
        "user": user,
        "posts": posts,
        "friends": CustomUser.objects.filter(id__in=friends),
        "is_friend": is_friend
    })

@login_required
def add_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if content or image:
            Post.objects.create(user=request.user, content=content, image=image)
            messages.success(request, "Запись опубликована!")
        else:
            messages.error(request, "Заполните текст поста или добавьте изображение!")

    return redirect("accounts:profile", user_id=request.user.id)


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_id = post.user.id  
    post.delete()
    return redirect('accounts:profile', user_id=user_id) 

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот пост.")

    if request.method == "POST":
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Пост успешно обновлён!")
            return redirect("accounts:profile", user_id=request.user.id)
    else:
        form = PostEditForm(instance=post)

    return render(request, "accounts/edit_post.html", {"form": form, "post": post})

def set_theme(request):
    theme = request.GET.get("theme", "light")
    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("accounts:settings")))
    response.set_cookie("theme", theme, max_age=31536000)
    return response
