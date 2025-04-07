from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render
from feed.models import Post

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должен быть email")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('user', 'Обычный пользователь'),
        ('expert', 'Эксперт'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор')
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    timezone = models.CharField(max_length=50, default='Asia/Almaty')
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True, default='profile_pics/def_icon.png')
    cover_photo = models.ImageField(upload_to='profile_pics', blank=True, null=True, default='images/default_cover.png')
    bio = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True, default="Статус Отсутствует!")  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False) 

    objects = CustomUserManager()  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.email

def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, "accounts/profile.html", {"user": user, "posts": posts})