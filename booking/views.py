from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.models import CustomUser
from .models import Booking
from .forms import BookingRequestForm, ConfirmBookingForm
from experts.models import Expert

@login_required
def request_booking(request, expert_id):
    expert = get_object_or_404(CustomUser, id=expert_id)
    if request.method == "POST":
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.expert = expert
            booking.scheduled_time = None  
            booking.status = "pending"
            booking.created_at = now()
            booking.save()
            
            expert_profile = get_object_or_404(Expert, user=expert)
            return redirect('experts:detail', pk=expert_profile.id)

        else:
            return render(request, "booking/request_booking.html", {"form": form, "expert": expert})
    else:
        form = BookingRequestForm()
    return render(request, "booking/request_booking.html", {"form": form, "expert": expert})



@login_required
def confirm_booking(request, booking_id):
    """
    Представление для подтверждения записи экспертом.
    Эксперт через форму назначает точное время консультации.
    После успешного подтверждения статус меняется на 'confirmed',
    создается консультационный чат (если его нет), и происходит редирект в комнату чата.
    """
    booking = get_object_or_404(Booking, id=booking_id, expert=request.user)
    if request.method == "POST":
        form = ConfirmBookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = "confirmed"
            booking.save()
            # Создаем консультационный чат, если он еще не создан
            from chat.models import Chat
            chat = Chat.objects.filter(chat_type='consultation', booking=booking).first()
            if not chat:
                chat = Chat.objects.create(chat_type='consultation', booking=booking)
                chat.participants.add(booking.user, booking.expert)
            return redirect('chat:chat_room', chat_id=chat.id)
    else:
        form = ConfirmBookingForm(instance=booking)
    return render(request, "booking/confirm_booking.html", {"form": form, "booking": booking})


@login_required
def handle_booking(request, booking_id, action):
    """
    Представление для обработки действий эксперта по заявке, например, отклонения.
    Здесь можно оставить логику для отклонения заявки.
    """
    booking = get_object_or_404(Booking, id=booking_id, expert=request.user)
    if action == "decline":
        booking.status = "canceled"
        booking.save()
        return JsonResponse({"message": "Заявка отклонена."})
    else:
        return JsonResponse({"error": "Недопустимое действие"}, status=400)


@login_required
def my_bookings(request):
    """
    Представление для отображения всех бронирований (запросов) для эксперта.
    """
    # Выбираем бронирования, где эксперт – залогиненный пользователь
    bookings = Booking.objects.filter(expert=request.user).order_by("-created_at")
    return render(request, "booking/my_bookings.html", {"bookings": bookings})