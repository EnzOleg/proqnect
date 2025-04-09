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


API_KEY = "2ffe04b830b8e9b0d2ea9b2fbb4105a3f90c1a4d9b5bafa61de80527ed4bfe4c"
BASE_URL = "https://api.daily.co/v1/rooms"

@api_view(["POST"])
def create_or_get_call(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    call = Call.objects.filter(chat=chat, is_active=True).first()
    if call:
        return Response({"room_url": call.room_url}) 

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "name": f"chat-call-{int(now().timestamp())}",
        "privacy": "public",
        "properties": {
            "enable_chat": True,
            "enable_knocking": False,
            "exp": int(now().timestamp()) + 7200  
        }
    }
    response = requests.post(BASE_URL, json=data, headers=headers)
    room_url = response.json().get("url")

    if room_url:
        Call.objects.create(chat=chat, room_url=room_url, is_active=True)
        return Response({"room_url": room_url})

    return Response({"error": "Не удалось создать комнату"}, status=500)

@api_view(["GET"])
def check_active_call(request, chat_id):
    active_call = Call.objects.filter(chat_id=chat_id, is_active=True).first()
    if active_call:
        return Response({"room_url": active_call.room_url})
    return Response({"room_url": None})

@api_view(["POST"])
def delete_call(request, chat_id):
    call = Call.objects.filter(chat_id=chat_id, is_active=True).first()
    if not call:
        return Response(status=404)

    headers = {"Authorization": f"Bearer {API_KEY}"}
    room_name = call.room_name
    requests.delete(f"{BASE_URL}/{room_name}", headers=headers)

    call.is_active = False
    call.save()

    return Response({"message": "Комната удалена"})


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