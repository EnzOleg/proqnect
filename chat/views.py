from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Chat

User = get_user_model()

@login_required
def chat_home(request):
    chats = Chat.objects.filter(participants=request.user).prefetch_related('participants').order_by("-updated_at")

    # Словарь {chat_id: собеседник}
    chat_partners = {chat.id: chat.get_chat_partner(request.user) for chat in chats}

    return render(request, "chat/chat_home.html", {
        "chats": chats,
        "chat_partners": chat_partners,  # Передаём в шаблон
    })


@login_required
def chat_room(request, chat_id):
    chat = get_object_or_404(Chat.objects.prefetch_related('participants'), id=chat_id)
    chat_partner = chat.get_chat_partner(request.user)
    sidebar_chats = Chat.objects.filter(participants=request.user).prefetch_related('participants').order_by("-updated_at")
    sidebar = [(c, c.get_chat_partner(request.user)) for c in sidebar_chats]
    
    return render(request, 'chat/chat_room.html', {
        'chat': chat,
        'chat_partner': chat_partner,
        'sidebar': sidebar,
    })



@login_required
def chat_with_user(request, user_id):
    """
    Создаёт или находит обычный (social) чат между текущим пользователем и пользователем с user_id.
    """
    other_user = get_object_or_404(User, pk=user_id)
    chat = Chat.objects.filter(chat_type='social', participants=request.user).filter(participants=other_user).first()

    if not chat:
        chat = Chat.objects.create(chat_type='social')
        chat.participants.add(request.user, other_user)
    
    return redirect('chat:chat_room', chat_id=chat.id)


@login_required
def consultation_chat_with_expert(request, user_id):
    """
    Создаёт или находит консультационный (рабочий) чат между текущим пользователем и экспертом.
    Если целевой пользователь не является экспертом, перенаправляет на обычный чат.
    """
    other_user = get_object_or_404(User, pk=user_id)

    if not hasattr(other_user, 'expert_profile'):
        return redirect('chat:chat_with_user', user_id=user_id)

    chat = Chat.objects.filter(chat_type='consultation', participants=request.user).filter(participants=other_user).first()
    
    if not chat:
        chat = Chat.objects.create(chat_type='consultation')
        chat.participants.add(request.user, other_user)
    
    return redirect('chat:chat_room', chat_id=chat.id)
