from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm
from .models import CustomUser, Post
from django.http import HttpResponseRedirect

def auth_view(request):
    form = CustomUserRegistrationForm()
    return render(request, "auth.html", {"form": form})

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
        else:
            for field, errors in form.errors.items():
                field_obj = form.fields.get(field)
                field_label = field_obj.label if field_obj and field_obj.label is not None else ""
                for error in errors:
                    if field_label:
                        messages.error(request, f"{field_label}: {error}")
                    else:
                        messages.error(request, error)
            return render(request, "auth.html", {"form": form, "show_register": True})
    return redirect("auth")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Неправильный email или пароль")
            return render(request, "auth.html", {"show_login": True})
    return redirect("auth")

@login_required
def settings_view(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.status = request.POST.get("status", user.status)
        if request.FILES.get("profile_picture"):
            user.profile_picture = request.FILES.get("profile_picture")
        user.save()
        messages.success(request, "Настройки обновлены!")
        return redirect("settings")
    
    return render(request, "settings.html")

def logout_view(request):
    logout(request)
    return redirect("auth")

@login_required
def profile_view(request):
    posts = request.user.posts.all().order_by("-created_at")
    friends = []  
    return render(request, "profile.html", {"user": request.user, "posts": posts, "friends": friends})

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
    return redirect("profile")

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('profile')

@login_required
def update_status(request):
    if request.method == "POST":
        request.user.status = request.POST.get("status", "").strip()
        request.user.save()
    return redirect('profile')

def set_theme(request):
    theme = request.GET.get("theme", "light")
    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    response.set_cookie("theme", theme, max_age=31536000)
    return response
