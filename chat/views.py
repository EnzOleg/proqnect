from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Call, Chat, Message
from django.contrib import messages
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

User = get_user_model()

@login_required
def chat_home(request):
    chats = Chat.objects.filter(participants=request.user).prefetch_related('participants').order_by("-updated_at")

    chats_with_partners = [
        {
            "chat": chat,
            "partner": chat.get_chat_partner(request.user),
            "avatar": chat.get_chat_partner(request.user).profile_picture.url if chat.get_chat_partner(request.user) else None
        }
        for chat in chats
    ]

    return render(request, "chat/chat_home.html", {
        "chats_with_partners": chats_with_partners,
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
    other_user = get_object_or_404(User, pk=user_id)

    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
    
    return redirect('chat:chat_room', chat_id=chat.id)

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.sender != request.user:
        messages.error(request, "У вас нет прав редактировать это сообщение.")
        return redirect('chat:chat_room', chat_id=message.chat.id)

    if request.method == "POST":
        new_text = request.POST.get("text")

        if new_text:
            message.text = new_text
            message.updated = True
            message.save()
            messages.success(request, "Сообщение обновлено.")
            return redirect('chat:chat_room', chat_id=message.chat.id)
        else:
            messages.error(request, "Сообщение не может быть пустым.")
    
    return render(request, "chat/edit_message.html", {
        'message': message
    })


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.sender != request.user:
        messages.error(request, "У вас нет прав удалить это сообщение.")
        return redirect('chat:chat_room', chat_id=message.chat.id)

    chat_id = message.chat.id
    message.delete()
    messages.success(request, "Сообщение удалено.")
    
    return redirect('chat:chat_room', chat_id=chat_id)