from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Friendship, FriendRequest
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def friend_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'friends/friend_requests.html', {'requests': requests})

@login_required
def add_friend(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if FriendRequest.objects.filter(from_user=request.user, to_user=user).exists():
        return redirect('accounts:profile', user_id=user.id)  # Уже отправлен запрос

    FriendRequest.objects.create(from_user=request.user, to_user=user)
    return redirect('accounts:profile', user_id=user.id)

@login_required
def accept_friend(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    Friendship.objects.create(user=request.user, friend=friend_request.from_user)
    Friendship.objects.create(user=friend_request.from_user, friend=request.user)
    friend_request.delete()
    return redirect('accounts:profile', user_id=request.user.id)

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    Friendship.objects.filter(user=request.user, friend=friend).delete()
    Friendship.objects.filter(user=friend, friend=request.user).delete()
    return redirect('accounts:profile', user_id=friend.id)
