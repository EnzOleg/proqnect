# proqnect/views.py
from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
from feed.models import Post  
from accounts.models import CustomUser  
from experts.models import Expert

def index(request):
    one_year_ago = now() - timedelta(days=365)
    
    post_count = Post.objects.filter(created_at__gte=one_year_ago).count()
    user_count = CustomUser.objects.filter(date_joined__gte=one_year_ago).count()
    expert_count = Expert.objects.filter(user__date_joined__gte=one_year_ago).count()

    context = {
        'post_count': post_count,
        'user_count': user_count,
        'expert_count': expert_count,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')
